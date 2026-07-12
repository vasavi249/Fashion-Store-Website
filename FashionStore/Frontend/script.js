const API_URL = 'http://127.0.0.1:8000';

const App = {
    state: {
        user: JSON.parse(localStorage.getItem('user')) || null,
        cart: JSON.parse(localStorage.getItem('cart')) || []
    },

    async api(endpoint, method = 'GET', data = null) {
        const url = `${API_URL}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error('API request failed');
            return await response.json();
        } catch (error) {
            this.showToast(error.message, 'error');
            throw error;
        }
    },

    setUser(user) {
        this.state.user = user;
        if(user) {
            localStorage.setItem('user', JSON.stringify(user));
        } else {
            localStorage.removeItem('user');
        }
        this.updateNav();
    },

    logout() {
        this.setUser(null);
        window.location.href = 'index.html';
    },

    updateNav() {
        const authLinks = document.getElementById('auth-links');
        if(!authLinks) return;
        
        if (this.state.user) {
            authLinks.innerHTML = `
                <div class="icon-btn" onclick="window.location.href='orders.html'">
                    <span>🛍️</span>
                    <span>Orders</span>
                </div>
                <div class="icon-btn" onclick="App.logout()">
                    <span>🚪</span>
                    <span>Logout</span>
                </div>
            `;
            if (this.state.user.role === 'admin' || this.state.user.email === 'admin@movies.com') {
                authLinks.innerHTML = `
                    <div class="icon-btn" onclick="window.location.href='dashboard.html'">
                        <span>⚙️</span>
                        <span>Admin</span>
                    </div>
                ` + authLinks.innerHTML;
            }
        } else {
            authLinks.innerHTML = `
                <div class="icon-btn" onclick="window.location.href='login.html'">
                    <span>👤</span>
                    <span>Profile</span>
                </div>
            `;
        }
    },

    async loadProducts(containerId) {
        const container = document.getElementById(containerId);
        if(!container) return;

        try {
            const products = await this.api('/products/');
            container.innerHTML = products.map(p => `
                <div class="product-card" onclick="window.location.href='product.html?id=${p.id}'">
                    <img src="${p.image_url}" alt="${p.product_name}" class="product-image">
                    <div class="product-info">
                        <div class="product-brand">${p.brand}</div>
                        <div class="product-name">${p.product_name}</div>
                        <div class="product-price">Rs. ${p.price}</div>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            container.innerHTML = '<p>Error loading products.</p>';
        }
    },

    showToast(msg, type = 'success') {
        let toast = document.getElementById('toast');
        if(!toast) {
            toast = document.createElement('div');
            toast.id = 'toast';
            toast.className = 'toast';
            document.body.appendChild(toast);
        }
        
        toast.className = `toast toast-${type} show`;
        toast.textContent = msg;
        
        setTimeout(() => {
            toast.className = `toast toast-${type}`;
        }, 3000);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    App.updateNav();
});
