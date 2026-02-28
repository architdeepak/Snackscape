const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// ── Middleware ────────────────────────────────────────────────────────────────
app.use(cors({ origin: true, credentials: true }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve the ssw/ folder as static files
app.use(express.static(path.join(__dirname, 'ssw')));
// Also serve root images for backward compat
app.use(express.static(path.join(__dirname)));

// ── Data Helpers ──────────────────────────────────────────────────────────────
const DATA_DIR = path.join(__dirname, 'data');

function readJSON(file) {
  try {
    return JSON.parse(fs.readFileSync(path.join(DATA_DIR, file), 'utf8'));
  } catch {
    return file === 'cart.json' ? {} : [];
  }
}

function writeJSON(file, data) {
  fs.writeFileSync(path.join(DATA_DIR, file), JSON.stringify(data, null, 2));
}

// ── Plans Data ────────────────────────────────────────────────────────────────
const PLANS = [
  {
    id: 'basic',
    name: 'Basic Plan',
    price: 20,
    items: 5,
    countries: 2,
    image: 'boxes1.png',
    description: 'Perfect for snack curious explorers sampling global flavors.',
    features: [
      '5 premium snacks per box',
      'From 2 different countries',
      'Flavor guide included',
      'Free shipping',
      'Cancel anytime'
    ]
  },
  {
    id: 'standard',
    name: 'Standard Plan',
    price: 30,
    items: 10,
    countries: 4,
    image: 'boxes2.png',
    description: 'The sweet spot for adventurous snackers who crave variety.',
    popular: true,
    features: [
      '10 premium snacks per box',
      'From 4 different countries',
      'Exclusive limited editions',
      'Priority shipping',
      'Recipe cards included',
      'Member community access'
    ]
  },
  {
    id: 'premium',
    name: 'Premium Plan',
    price: 45,
    items: 20,
    countries: 6,
    image: 'boxes3.png',
    description: 'The ultimate snack experience with rare finds worldwide.',
    features: [
      '20 premium snacks per box',
      'From 6+ different countries',
      'VIP-only rare snacks',
      'Express shipping',
      'Exclusive merch item',
      'Early access to new drops',
      'Members-only events',
      'Quarterly bonus box'
    ]
  }
];

// ── Reviews Data ──────────────────────────────────────────────────────────────
const REVIEWS = [
  { name: 'Arjun M.', rating: 5, text: 'Every box is a wild ride. Got Japanese wasabi chips that changed my life forever.', plan: 'Premium', country: '🇮🇳' },
  { name: 'Sofia L.', rating: 5, text: 'The Korean seaweed snacks are absolutely addictive. I order 3 boxes now.', plan: 'Standard', country: '🇧🇷' },
  { name: 'Tyler B.', rating: 5, text: 'Opened my box and literally yelled. Ghost pepper crisps from Mexico are NO JOKE.', plan: 'Premium', country: '🇺🇸' },
  { name: 'Priya S.', rating: 5, text: 'Best subscription I have ever owned. My friends keep stealing my snacks.', plan: 'Basic', country: '🇮🇳' },
  { name: 'Lucas R.', rating: 5, text: 'UK biscuits, Thai chips, Israeli chocolate — the curation is unreal.', plan: 'Standard', country: '🇨🇱' },
  { name: 'Mei C.', rating: 5, text: 'I travel for work so this is how I keep getting global flavors at home.', plan: 'Premium', country: '🇨🇳' },
  { name: 'Jake T.', rating: 4, text: 'Massive boxes, insane variety. The packaging alone is Instagram-worthy.', plan: 'Standard', country: '🇨🇦' },
  { name: 'Nadia K.', rating: 5, text: 'My kids fight over the snacks every single month. 10/10 family chaos.', plan: 'Premium', country: '🇩🇪' }
];

// ── Rate Limiters ─────────────────────────────────────────────────────────────
const contactLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 5, message: { error: 'Too many requests, try again later.' } });
const newsletterLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 3, message: { error: 'Too many requests, try again later.' } });

// ── Cart Cookie Helper ────────────────────────────────────────────────────────
function getCartId(req, res) {
  let cartId = req.headers['x-cart-id'];
  if (!cartId) {
    cartId = uuidv4();
  }
  res.setHeader('X-Cart-Id', cartId);
  return cartId;
}

// ── Routes ────────────────────────────────────────────────────────────────────

// GET /api/plans
app.get('/api/plans', (req, res) => {
  res.json({ success: true, plans: PLANS });
});

// GET /api/reviews
app.get('/api/reviews', (req, res) => {
  res.json({ success: true, reviews: REVIEWS });
});

// GET /api/cart
app.get('/api/cart', (req, res) => {
  const cartId = getCartId(req, res);
  const allCarts = readJSON('cart.json');
  const cart = allCarts[cartId] || [];
  const total = cart.reduce((sum, item) => sum + item.price, 0);
  res.json({ success: true, cartId, cart, total });
});

// POST /api/cart  — body: { planId, planName, price, image }
app.post('/api/cart', (req, res) => {
  const { planId, planName, price, image } = req.body;
  if (!planId || !planName || price == null) {
    return res.status(400).json({ error: 'Missing planId, planName, or price' });
  }

  const cartId = getCartId(req, res);
  const allCarts = readJSON('cart.json');
  const cart = allCarts[cartId] || [];

  if (cart.find(i => i.planId === planId)) {
    return res.status(409).json({ error: 'Plan already in cart' });
  }

  const item = { id: uuidv4(), planId, planName, price, image: image || 'boxes1.png', addedAt: new Date().toISOString() };
  cart.push(item);
  allCarts[cartId] = cart;
  writeJSON('cart.json', allCarts);

  const total = cart.reduce((sum, i) => sum + i.price, 0);
  res.json({ success: true, cartId, item, cart, total });
});

// DELETE /api/cart/:itemId
app.delete('/api/cart/:itemId', (req, res) => {
  const cartId = getCartId(req, res);
  const allCarts = readJSON('cart.json');
  const cart = allCarts[cartId] || [];
  const idx = cart.findIndex(i => i.id === req.params.itemId);
  if (idx === -1) return res.status(404).json({ error: 'Item not found' });
  const removed = cart.splice(idx, 1)[0];
  allCarts[cartId] = cart;
  writeJSON('cart.json', allCarts);
  const total = cart.reduce((sum, i) => sum + i.price, 0);
  res.json({ success: true, removed, cart, total });
});

// DELETE /api/cart  — clear cart
app.delete('/api/cart', (req, res) => {
  const cartId = getCartId(req, res);
  const allCarts = readJSON('cart.json');
  allCarts[cartId] = [];
  writeJSON('cart.json', allCarts);
  res.json({ success: true, cart: [], total: 0 });
});

// POST /api/checkout  — body: { customer: { name, email, address }, cart }
app.post('/api/checkout', (req, res) => {
  const { customer, cart } = req.body;
  if (!customer?.name || !customer?.email || !cart?.length) {
    return res.status(400).json({ error: 'Missing customer info or empty cart' });
  }

  const order = {
    id: uuidv4(),
    customer,
    cart,
    total: cart.reduce((sum, i) => sum + i.price, 0),
    status: 'confirmed',
    createdAt: new Date().toISOString()
  };

  const orders = readJSON('orders.json');
  orders.push(order);
  writeJSON('orders.json', orders);

  // Clear cart
  const cartId = req.headers['x-cart-id'];
  if (cartId) {
    const allCarts = readJSON('cart.json');
    allCarts[cartId] = [];
    writeJSON('cart.json', allCarts);
  }

  res.json({ success: true, order });
});

// POST /api/contact  — body: { name, email, subject, message }
app.post('/api/contact', contactLimiter, (req, res) => {
  const { name, email, subject, message } = req.body;
  if (!name || !email || !message) {
    return res.status(400).json({ error: 'name, email, and message are required' });
  }

  const entry = { id: uuidv4(), name, email, subject: subject || 'General', message, createdAt: new Date().toISOString() };
  const messages = readJSON('messages.json');
  messages.push(entry);
  writeJSON('messages.json', messages);

  res.json({ success: true, message: 'Message received! We will reply within 24 hours.' });
});

// POST /api/newsletter  — body: { email }
app.post('/api/newsletter', newsletterLimiter, (req, res) => {
  const { email } = req.body;
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Valid email required' });
  }

  const messages = readJSON('messages.json');
  const existing = messages.find(m => m.type === 'newsletter' && m.email === email);
  if (existing) {
    return res.status(409).json({ error: 'Already subscribed!' });
  }

  messages.push({ id: uuidv4(), type: 'newsletter', email, createdAt: new Date().toISOString() });
  writeJSON('messages.json', messages);

  res.json({ success: true, message: 'You are subscribed! Welcome to the chaos.' });
});

// ── Start Server ──────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`\n🍿 Snackscape backend running at http://localhost:${PORT}`);
  console.log(`   Frontend: http://localhost:${PORT}/Snackscapewebsite.html\n`);
});
