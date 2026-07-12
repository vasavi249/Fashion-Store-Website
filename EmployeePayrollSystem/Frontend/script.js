const API_URL = 'http://127.0.0.1:8000';

const App = {
    state: {
        user: JSON.parse(localStorage.getItem('emp_user')) || null
    },

    async api(endpoint, method = 'GET', data = null) {
        const url = `${API_URL}${endpoint}`;
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (data) options.body = JSON.stringify(data);

        try {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error('API Error');
            return await response.json();
        } catch (error) {
            this.showToast(error.message, 'error');
            throw error;
        }
    },

    setUser(user) {
        this.state.user = user;
        if(user) {
            localStorage.setItem('emp_user', JSON.stringify(user));
        } else {
            localStorage.removeItem('emp_user');
        }
        this.updateNav();
    },

    logout() {
        this.setUser(null);
        window.location.href = 'index.html';
    },

    updateNav() {
        const links = document.getElementById('nav-links');
        const auth = document.getElementById('auth-buttons');
        
        if(!links || !auth) return;

        if (this.state.user) {
            if(this.state.user.role === 'admin') {
                links.innerHTML = `
                    <a href="dashboard.html">Dashboard</a>
                    <a href="employees.html">Employees</a>
                    <a href="departments.html">Departments</a>
                    <a href="attendance.html">Attendance</a>
                    <a href="payroll.html">Payroll</a>
                `;
            } else {
                links.innerHTML = `
                    <a href="attendance.html">My Attendance</a>
                    <a href="payslips.html">My Payslips</a>
                `;
            }
            
            auth.innerHTML = `
                <span style="margin-right: 15px; font-weight: 600;">Welcome, ${this.state.user.full_name}</span>
                <button class="btn btn-outline" onclick="App.logout()">Logout</button>
            `;
        } else {
            links.innerHTML = ``;
            auth.innerHTML = `
                <button class="btn btn-outline" onclick="window.location.href='index.html'">Login</button>
            `;
        }
    },

    showToast(msg, type = 'success') {
        let toast = document.getElementById('toast');
        if(!toast) {
            toast = document.createElement('div');
            toast.id = 'toast';
            document.body.appendChild(toast);
        }
        toast.className = `toast toast-${type} show`;
        toast.textContent = msg;
        setTimeout(() => toast.className = `toast toast-${type}`, 3000);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    App.updateNav();
});
