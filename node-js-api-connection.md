

````markdown
# Django Data Display with Node.js Express

This project shows how to build a Node.js Express server that fetches data from a Django REST API and displays it using EJS templates.

---

## 📦 1. Set Up Your Node.js Express Server

### ✅ Prerequisites

Ensure you have Node.js and npm installed. You can download them from [https://nodejs.org/](https://nodejs.org/).

---

### 🛠️ Step 1: Create and Initialize the Project

```bash
mkdir django-data-display
cd django-data-display
npm init -y
````

---

### 📦 Step 2: Install Dependencies

```bash
npm install express axios ejs / npm install express axios ejs bootstrap@5
```

**Dependencies:**

* `express`: For creating the web server.
* `axios`: For making HTTP requests to the Django API.
* `ejs`: For rendering server-side HTML.

---

### 📁 Step 3: Create `server.js`

Create a file named `server.js` in the root of your project:

```js
const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000; // You can change this if needed

// Set EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

// Route to fetch and display data from Django API
app.get('/display-data', async (req, res) => {
  try {
    const djangoApiUrl = 'YOUR_DJANGO_API_ENDPOINT_HERE'; // Replace with your actual API URL
    const response = await axios.get(djangoApiUrl);
    const data = response.data;

    res.render('display', { data: data });
  } catch (error) {
    console.error('Error fetching data:', error.message);
    res.status(500).send('Error fetching data from Django API');
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
```

---

## 🖼️ 2. Create an EJS View Template

### 📁 Step 1: Create the `views` Directory

```bash
mkdir views
```

---

### 📝 Step 2: Create `display.ejs`

Inside the `views` folder, create a file called `display.ejs`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Data from Django API</title>
</head>
<body>
  <h1>Data from Django API</h1>

  <% if (data && data.length > 0) { %>
    <ul>
      <% data.forEach(item => { %>
        <li><%= JSON.stringify(item) %></li>
      <% }); %>
    </ul>
  <% } else if (data && Object.keys(data).length > 0) { %>
    <pre><%= JSON.stringify(data, null, 2) %></pre>
  <% } else { %>
    <p>No data available.</p>
  <% } %>
</body>
</html>
```

---

## 🚀 3. Replace Placeholder and Run

### 📝 Replace Placeholder

In `server.js`, replace:

```js
const djangoApiUrl = 'YOUR_DJANGO_API_ENDPOINT_HERE';
```

With the actual Django API URL, such as:

```js
const djangoApiUrl = 'http://127.0.0.1:8000/api/your-endpoint/';
```

Make sure your Django backend server is running and accessible.

---

### ▶️ Run the Node Server

From the root directory:

```bash
node server.js
```

You should see:

```
Server running at http://localhost:3000
```

---

## 🌐 4. Access the App in Browser

Visit:

```
http://localhost:3000/display-data
```

You should see the data fetched from your Django API rendered on the page.

---

## ⚠️ Important Considerations

* **CORS**: If the Django and Node.js servers run on different domains/ports, configure [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) in Django using the `django-cors-headers` package.
* **Error Handling**: Improve server reliability by adding better error handling/logging.
* **Data Formatting**: Customize the EJS template based on your API's data structure.
* **Security**: Don’t expose API secrets or sensitive data on the client side.
* **Styling**: Add CSS to `display.ejs` or link external stylesheets to improve appearance.

---

## ✅ Final Directory Structure

```
django-data-display/
├── node_modules/
├── views/
│   └── display.ejs
├── server.js
├── package.json
└── README.md
```

---

## 🎉 You're Done!

You now have a basic Node.js + Express app that fetches data from a Django API and displays it using EJS. Feel free to expand this into a more advanced full-stack application!

```

Let me know if you'd like me to generate a `.zip` project structure or upload this file directly.
```
