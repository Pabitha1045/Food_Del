const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const axios = require('axios');
const jwt = require('jsonwebtoken');

const app = express();
const PORT = process.env.PORT || 5002;

// Middleware
app.use(cors());
app.use(express.json());

// Auth middleware
const auth = (req, res, next) => {
  const token = req.header('Authorization')?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ message: 'No token provided' });
  try {
    const decoded = jwt.verify(token, 'secretkey');
    req.userId = decoded.userId;
    next();
  } catch (error) {
    res.status(401).json({ message: 'Invalid token' });
  }
};

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/food-delivery-orders', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('Orders MongoDB connected'))
.catch(err => console.log(err));

// Order model
const orderSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, required: true },
  restaurant: { type: String, required: true },
  items: [{ menuItem: String, quantity: Number, price: Number }],
  totalAmount: { type: Number, required: true },
  status: { type: String, enum: ['pending', 'confirmed', 'preparing', 'delivered', 'cancelled'], default: 'pending' },
  deliveryAddress: { type: String, required: true },
}, { timestamps: true });

const Order = mongoose.model('Order', orderSchema);

// Routes
app.post('/orders', auth, async (req, res) => {
  try {
    const { restaurant, items, deliveryAddress } = req.body;
    const totalAmount = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const order = new Order({
      user: req.userId,
      restaurant,
      items,
      totalAmount,
      deliveryAddress,
    });
    await order.save();
    res.status(201).json(order);
  } catch (error) {
    res.status(500).json({ message: 'Error creating order' });
  }
});

app.get('/orders', auth, async (req, res) => {
  try {
    const orders = await Order.find({ user: req.userId });
    res.json(orders);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching orders' });
  }
});

// Proxy to restaurant service
app.get('/restaurants', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:8001/api/restaurants');
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching restaurants' });
  }
});

app.listen(PORT, () => {
  console.log(`Orders service running on port ${PORT}`);
});
