// API Base URL
const API_BASE_URL = 'http://localhost:5000/api';

// State
let authToken = localStorage.getItem('authToken');
let currentUser = null;
let currentPage = 1;
let currentFilters = {};

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        loadDashboard();
    } else {
        showAuthPage();
    }

    setupEventListeners();
});

function setupEventListeners() {
    // Login form
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        await login(username, password);
    });

    // Register form
    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        await register(username, email, password);
    });

    // Scraping form
    document.getElementById('scraping-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = document.getElementById('scrape-url').value;
        const merchant = document.getElementById('scrape-merchant').value;
        const pages = document.getElementById('scrape-pages').value;
        await startScraping(url, merchant, pages);
    });
}

// Auth functions
function showLoginForm() {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
    document.querySelectorAll('.tab')[0].classList.add('active');
    document.getElementById('login-form').classList.add('active');
}

function showRegisterForm() {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
    document.querySelectorAll('.tab')[1].classList.add('active');
    document.getElementById('register-form').classList.add('active');
}

async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            currentUser = data.user;
            loadDashboard();
        } else {
            document.getElementById('login-error').textContent = data.error || 'Login failed';
        }
    } catch (error) {
        document.getElementById('login-error').textContent = 'Network error. Please try again.';
    }
}

async function register(username, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            currentUser = data.user;
            loadDashboard();
        } else {
            document.getElementById('register-error').textContent = data.error || 'Registration failed';
        }
    } catch (error) {
        document.getElementById('register-error').textContent = 'Network error. Please try again.';
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showAuthPage();
}

function showAuthPage() {
    document.getElementById('auth-page').classList.add('active');
    document.getElementById('dashboard-page').classList.remove('active');
}

// Dashboard functions
async function loadDashboard() {
    document.getElementById('auth-page').classList.remove('active');
    document.getElementById('dashboard-page').classList.add('active');
    showDashboard();
}

async function showDashboard() {
    hideAllSections();
    document.getElementById('dashboard-section').classList.add('active');
    await loadStatistics();
}

async function showInventory() {
    hideAllSections();
    document.getElementById('inventory-section').classList.add('active');
    await loadInventory();
}

async function showScraping() {
    hideAllSections();
    document.getElementById('scraping-section').classList.add('active');
    await loadScrapingJobs();
}

function hideAllSections() {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
}

// Statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            updateStatistics(data);
        }
    } catch (error) {
        console.error('Failed to load statistics:', error);
    }
}

function updateStatistics(data) {
    document.getElementById('stat-total-items').textContent = data.total_items || 0;
    document.getElementById('stat-total-value').textContent = `$${data.total_value || 0}`;
    document.getElementById('stat-sold-items').textContent = data.sold_items || 0;
    document.getElementById('stat-scraping-jobs').textContent = data.total_scraping_jobs || 0;

    // Merchant chart
    const merchantChart = document.getElementById('merchant-chart');
    merchantChart.innerHTML = '';
    if (data.items_by_merchant && data.items_by_merchant.length > 0) {
        data.items_by_merchant.forEach(item => {
            const bar = document.createElement('div');
            bar.style.cssText = `
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #e5e7eb;
            `;
            bar.innerHTML = `
                <span>${item.merchant}</span>
                <span style="font-weight: bold;">${item.count}</span>
            `;
            merchantChart.appendChild(bar);
        });
    } else {
        merchantChart.innerHTML = '<p style="color: #6b7280;">No data available</p>';
    }

    // Condition chart
    const conditionChart = document.getElementById('condition-chart');
    conditionChart.innerHTML = '';
    if (data.items_by_condition && data.items_by_condition.length > 0) {
        data.items_by_condition.forEach(item => {
            const bar = document.createElement('div');
            bar.style.cssText = `
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #e5e7eb;
            `;
            bar.innerHTML = `
                <span>${item.condition}</span>
                <span style="font-weight: bold;">${item.count}</span>
            `;
            conditionChart.appendChild(bar);
        });
    } else {
        conditionChart.innerHTML = '<p style="color: #6b7280;">No data available</p>';
    }

    // Recent items
    const recentItemsList = document.getElementById('recent-items-list');
    recentItemsList.innerHTML = '';
    if (data.recent_items && data.recent_items.length > 0) {
        data.recent_items.forEach(item => {
            const itemRow = document.createElement('div');
            itemRow.className = 'item-row';
            itemRow.innerHTML = `
                <div class="item-info">
                    <h4>${item.title}</h4>
                    <p>${item.merchant} • ${item.condition}</p>
                </div>
                <div class="item-price">$${item.price || 0}</div>
            `;
            recentItemsList.appendChild(itemRow);
        });
    } else {
        recentItemsList.innerHTML = '<p style="color: #6b7280;">No items yet</p>';
    }
}

// Inventory
async function loadInventory(page = 1) {
    currentPage = page;
    try {
        const params = new URLSearchParams({
            page: page,
            per_page: 20,
            ...currentFilters
        });

        const response = await fetch(`${API_BASE_URL}/inventory?${params}`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            displayInventory(data);
        }
    } catch (error) {
        console.error('Failed to load inventory:', error);
    }
}

function displayInventory(data) {
    const tbody = document.getElementById('inventory-tbody');
    tbody.innerHTML = '';

    if (data.items && data.items.length > 0) {
        data.items.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${item.title}</td>
                <td>$${item.price || 0}</td>
                <td>${item.merchant || 'N/A'}</td>
                <td>${item.condition || 'N/A'}</td>
                <td>
                    <span class="status-badge ${item.is_sold ? 'sold' : 'available'}">
                        ${item.is_sold ? 'Sold' : 'Available'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-danger" onclick="deleteItem(${item.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } else {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No items found</td></tr>';
    }

    // Pagination
    displayPagination(data);
}

function displayPagination(data) {
    const pagination = document.getElementById('inventory-pagination');
    pagination.innerHTML = '';

    if (data.pages > 1) {
        for (let i = 1; i <= data.pages; i++) {
            const btn = document.createElement('button');
            btn.textContent = i;
            btn.className = i === currentPage ? 'active' : '';
            btn.onclick = () => loadInventory(i);
            pagination.appendChild(btn);
        }
    }
}

function applyFilters() {
    const search = document.getElementById('search-input').value;
    const merchant = document.getElementById('merchant-filter').value;
    const condition = document.getElementById('condition-filter').value;

    currentFilters = {};
    if (search) currentFilters.search = search;
    if (merchant) currentFilters.merchant = merchant;
    if (condition) currentFilters.condition = condition;

    loadInventory(1);
}

async function deleteItem(itemId) {
    if (!confirm('Are you sure you want to delete this item?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/inventory/${itemId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            loadInventory(currentPage);
        }
    } catch (error) {
        console.error('Failed to delete item:', error);
    }
}

async function exportInventory() {
    alert('Export functionality would download a CSV file. Not fully implemented in this demo.');
}

// Scraping
async function startScraping(url, merchant, pages) {
    const messageDiv = document.getElementById('scraping-message');
    messageDiv.textContent = 'Starting scraping job...';
    messageDiv.className = 'message';

    try {
        const response = await fetch(`${API_BASE_URL}/scraping/scrape`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url, merchant, pages: parseInt(pages) })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = 'Scraping job started successfully!';
            messageDiv.className = 'message success';
            setTimeout(() => {
                loadScrapingJobs();
            }, 2000);
        } else {
            messageDiv.textContent = data.error || 'Failed to start scraping';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        messageDiv.textContent = 'Network error. Please try again.';
        messageDiv.className = 'message error';
    }
}

async function loadScrapingJobs() {
    try {
        const response = await fetch(`${API_BASE_URL}/scraping/jobs`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });

        if (response.ok) {
            const data = await response.json();
            displayScrapingJobs(data.jobs);
        }
    } catch (error) {
        console.error('Failed to load scraping jobs:', error);
    }
}

function displayScrapingJobs(jobs) {
    const tbody = document.getElementById('scraping-jobs-tbody');
    tbody.innerHTML = '';

    if (jobs && jobs.length > 0) {
        jobs.forEach(job => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${job.url}</td>
                <td>${job.merchant}</td>
                <td class="status-${job.status}">${job.status}</td>
                <td>${job.items_scraped || 0}</td>
                <td>${new Date(job.created_at).toLocaleString()}</td>
            `;
            tbody.appendChild(tr);
        });
    } else {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No scraping jobs yet</td></tr>';
    }
}
