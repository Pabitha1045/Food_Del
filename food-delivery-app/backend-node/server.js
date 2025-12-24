const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/food-delivery', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('MongoDB connected'))
.catch(err => console.log(err));

// Routes
app.use('/api/auth', require('./routes/auth'));
app.use('/api/orders', require('./routes/orders'));

// Proxy to Python backend for restaurant data
app.get('/api/restaurants', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:8000/api/restaurants');
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching restaurants' });
  }
});

app.listen(PORT, () => {
  console.log(`Node.js backend running on port ${PORT}`);
});
