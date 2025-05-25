from flask import Flask, request, jsonify, render_template_string
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# 🧁 Our cute HTML lives right here
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Scrape-o-Tron 3000 🌈</title>
  <style>
    body {
      font-family: 'Comic Sans MS', cursive, sans-serif;
      background: linear-gradient(135deg, #fef6ff, #e0f7fa);
      text-align: center;
      padding: 40px;
      color: #333;
    }

    h1 {
      font-size: 2.5rem;
      color: #ff69b4;
      margin-bottom: 20px;
    }

    img {
      width: 150px;
      margin-bottom: 20px;
      animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
      0% { transform: translateY(0px); }
      50% { transform: translateY(-10px); }
      100% { transform: translateY(0px); }
    }

    input, button {
      padding: 12px;
      margin: 10px;
      width: 300px;
      font-size: 1rem;
      border: none;
      border-radius: 10px;
      box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }

    input {
      background: #ffffff;
      color: #333;
    }

    button {
      background-color: #ffb347;
      color: white;
      font-weight: bold;
      cursor: pointer;
      transition: background 0.3s ease;
    }

    button:hover {
      background-color: #ffa500;
    }

    #output {
      margin-top: 30px;
      padding: 20px;
      background: #fffaf0;
      border: 2px dashed #f48fb1;
      border-radius: 12px;
      max-width: 800px;
      margin-left: auto;
      margin-right: auto;
      text-align: left;
      white-space: pre-wrap;
      box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <h1>🧠 Scrape-o-Tron 3000</h1>
  <img src="https://cdn.pixabay.com/photo/2021/06/23/06/51/cartoon-6359356_1280.png" alt="Cute Bot" />
  
  <form id="scrapeForm">
    <input type="text" name="url" placeholder="Paste your URL here!" required />
    <button type="submit">Scrape It! 🚀</button>
  </form>

  <div id="output">📝 Scraped content will show up here...</div>

  <script>
    const form = document.getElementById('scrapeForm');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const url = formData.get('url');
      const output = document.getElementById('output');
      output.textContent = 'Scraping... hold tight! 🌀';

      try {
        const response = await fetch('/scrape', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url })
        });

        const data = await response.json();
        output.textContent = data.result || 'No content found.';
      } catch (err) {
        output.textContent = '🚨 Error: ' + err.message;
      }
    });
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'result': 'No URL provided.'})

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'result': f'Error: Status code {response.status_code}'})

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = '\n\n'.join([p.get_text() for p in paragraphs[:15]])  # Limit to first 15

        return jsonify({'result': content})
    except Exception as e:
        return jsonify({'result': f'Something went wrong: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)