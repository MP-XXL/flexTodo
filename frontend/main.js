    // ── CONFIG ────────────────────────────────────────────────────────
    // In production this points to your Render backend URL.
  
    const API = "https://flextodo.onrender.com/api/v1" || 'http://localhost:8000/api/v1'
    // ─────────────────────────────────────────────────────────────────

    // ── STORAGE ───────────────────────────────────────────────────────
    const getToken = () => localStorage.getItem('flextodo_token')
    const setToken = t  => localStorage.setItem('flextodo_token', t)
    const clearToken = () => localStorage.removeItem('flextodo_token')
    const getUser   = () => JSON.parse(localStorage.getItem('flextodo_user') || 'null')
    const setUser   = u  => localStorage.setItem('flextodo_user', JSON.stringify(u))
    const clearUser = () => localStorage.removeItem('flextodo_user')

    const authHeaders = () => ({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`
    })

    // ── API WRAPPER ───────────────────────────────────────────────────
    async function apiFetch(path, options = {}) {
      try {
        const res  = await fetch(`${API}${path}`, options)
        const data = await res.json()
        if (!res.ok) {
          const msg = data.detail || 'Something went wrong.'
          throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg))
        }
        return data
      } catch (err) {
        if (err instanceof TypeError) throw new Error('Network error. Is the API reachable?')
        throw err
      }
    }

    // ── UI HELPERS ────────────────────────────────────────────────────
    const showEl = id => document.getElementById(id).classList.remove('hidden')
    const hideEl = id => document.getElementById(id).classList.add('hidden')

    function showError(id, msg) {
      const el = document.getElementById(id)
      el.textContent = msg
      el.classList.remove('hidden')
    }
    const hideError = id => document.getElementById(id).classList.add('hidden')

    // ── NAV ───────────────────────────────────────────────────────────
    function renderNav() {
      const nav  = document.getElementById('nav-auth')
      const user = getUser()
      if (user) {
        nav.innerHTML = `
          <span class="text-zinc-400 text-sm hidden sm:inline">
            ${escHtml(user.first_name)} ${escHtml(user.last_name)}
          </span>
          <button onclick="showView('todos')" class="text-sm text-zinc-300 hover:text-white transition-colors">My Todos</button>
          <button onclick="showView('guest')" class="text-sm text-zinc-300 hover:text-white transition-colors">Guest Todos</button>
          <button onclick="logout()" class="text-sm text-zinc-500 hover:text-red-400 transition-colors">Logout</button>
        `
      } else {
        nav.innerHTML = `
          <button onclick="showView('auth')" class="text-sm text-zinc-300 hover:text-white transition-colors">Login</button>
          <button onclick="showView('guest')" class="text-sm text-zinc-300 hover:text-white transition-colors">Guest Todos</button>
        `
      }
    }

    // ── VIEWS ─────────────────────────────────────────────────────────
    function showView(view) {
      hideEl('section-auth')
      hideEl('section-todos')
      hideEl('section-guest')
      if (view === 'auth')  showEl('section-auth')
      if (view === 'todos') { showEl('section-todos'); loadTodos() }
      if (view === 'guest') { showEl('section-guest'); loadGuestTodos() }
    }

    // ── TAB SWITCHING ─────────────────────────────────────────────────
    function switchTab(tab) {
      const active   = 'bg-zinc-800 text-white'
      const inactive = 'text-zinc-400 hover:text-white'
      if (tab === 'login') {
        showEl('form-login');    hideEl('form-register')
        document.getElementById('tab-login').className    = `px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${active}`
        document.getElementById('tab-register').className = `px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${inactive}`
      } else {
        hideEl('form-login');    showEl('form-register')
        document.getElementById('tab-register').className = `px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${active}`
        document.getElementById('tab-login').className    = `px-4 py-1.5 rounded-md text-sm font-medium transition-colors ${inactive}`
      }
    }

    // ── AUTH ──────────────────────────────────────────────────────────
    async function handleLogin(e) {
      e.preventDefault()
      hideError('login-error')
      const btn = document.getElementById('login-btn')
      btn.disabled = true; btn.textContent = 'Logging in…'
      try {
        const tokenData = await apiFetch('/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email:    document.getElementById('login-email').value.trim(),
            password: document.getElementById('login-password').value
          })
        })
        setToken(tokenData.access_token)
        const user = await apiFetch('/auth/me', { headers: authHeaders() })
        setUser(user)
        renderNav()
        showView('todos')
      } catch (err) {
        clearToken(); clearUser()
        showError('login-error', err.message)
      } finally {
        btn.disabled = false; btn.textContent = 'Login'
      }
    }

    async function handleRegister(e) {
      e.preventDefault()
      hideError('register-error'); hideEl('register-success')
      const btn = document.getElementById('register-btn')
      btn.disabled = true; btn.textContent = 'Creating account…'
      try {
        const data = await apiFetch('/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            first_name: document.getElementById('reg-first').value.trim(),
            last_name:  document.getElementById('reg-last').value.trim(),
            email:      document.getElementById('reg-email').value.trim(),
            password:   document.getElementById('reg-password').value
          })
        })
        setUser(data.user)
        document.getElementById('register-success').textContent = 'Account created! You can now log in.'
        showEl('register-success')
        setTimeout(() => switchTab('login'), 1200)
      } catch (err) {
        showError('register-error', err.message)
      } finally {
        btn.disabled = false; btn.textContent = 'Create account'
      }
    }

    function logout() {
      clearToken(); clearUser()
      renderNav()
      showView('auth')
      switchTab('login')
    }

    // ── USER TODOS ────────────────────────────────────────────────────
    async function loadTodos() {
      const user = getUser()
      document.getElementById('user-greeting').textContent =
        user ? `Hello, ${user.first_name} ${user.last_name}` : ''

      document.getElementById('todo-list').innerHTML = ''
      hideEl('todo-empty'); showEl('todo-loading')

      try {
        const data  = await apiFetch('/todos', { headers: authHeaders() })
        hideEl('todo-loading')
        const todos = data.todos || []
        todos.length === 0 ? showEl('todo-empty') : renderTodos(todos)
      } catch (err) {
        hideEl('todo-loading')
        if (err.message.toLowerCase().includes('credentials') || err.message.includes('401')) {
          logout()
        } else {
          document.getElementById('todo-list').innerHTML =
            `<p class="text-red-400 text-sm">${escHtml(err.message)}</p>`
        }
      }
    }

    function renderTodos(todos) {
      document.getElementById('todo-list').innerHTML = todos.map(todo => `
        <div id="todo-${todo.id}" class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 flex items-start gap-4 fade-in">
          <button onclick="toggleTodo(${todo.id}, '${todo.status}')" title="Toggle status"
            class="mt-0.5 w-5 h-5 rounded-full border-2 flex-shrink-0 transition-colors ${
              todo.status === 'COMPLETED' ? 'bg-amber-400 border-amber-400' : 'border-zinc-600 hover:border-amber-400'
            }"></button>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium ${todo.status === 'COMPLETED' ? 'line-through text-zinc-500' : 'text-white'}">
              ${escHtml(todo.title)}
            </p>
            <p class="text-xs text-zinc-500 mt-0.5">${escHtml(todo.body)}</p>
          </div>
          <span class="mono text-xs px-2 py-0.5 rounded-md flex-shrink-0 ${
            todo.status === 'COMPLETED' ? 'bg-zinc-800 text-zinc-500' : 'bg-amber-400/10 text-amber-400'
          }">${todo.status}</span>
          <button onclick="deleteTodo(${todo.id})" title="Delete"
            class="text-zinc-600 hover:text-red-400 transition-colors flex-shrink-0 text-xl leading-none">&times;</button>
        </div>
      `).join('')
    }

    async function handleCreateTodo() {
      hideError('todo-create-error')
      const title = document.getElementById('todo-title').value.trim()
      const body  = document.getElementById('todo-body').value.trim()
      if (!title || !body) { showError('todo-create-error', 'Title and description are required.'); return }
      try {
        await apiFetch('/todos', {
          method: 'POST', headers: authHeaders(),
          body: JSON.stringify({ title, body, status: 'PENDING' })
        })
        document.getElementById('todo-title').value = ''
        document.getElementById('todo-body').value  = ''
        await loadTodos()
      } catch (err) { showError('todo-create-error', err.message) }
    }

    async function toggleTodo(id, currentStatus) {
      try {
        await apiFetch(`/todos/${id}`, {
          method: 'PUT', headers: authHeaders(),
          body: JSON.stringify({ status: currentStatus === 'PENDING' ? 'COMPLETED' : 'PENDING' })
        })
        await loadTodos()
      } catch (err) { alert(err.message) }
    }

    async function deleteTodo(id) {
      try {
        await apiFetch(`/todos/${id}`, { method: 'DELETE', headers: authHeaders() })
        await loadTodos()
      } catch (err) { alert(err.message) }
    }

    // ── GUEST TODOS ───────────────────────────────────────────────────
    async function loadGuestTodos() {
      document.getElementById('guest-todo-list').innerHTML = ''
      hideEl('guest-empty'); showEl('guest-loading')
      try {
        const data  = await apiFetch('/guest/todos')
        hideEl('guest-loading')
        const todos = data.todos || []
        todos.length === 0 ? showEl('guest-empty') : renderGuestTodos(todos)
      } catch (err) {
        hideEl('guest-loading')
        document.getElementById('guest-todo-list').innerHTML =
          `<p class="text-red-400 text-sm">${escHtml(err.message)}</p>`
      }
    }

    function renderGuestTodos(todos) {
      document.getElementById('guest-todo-list').innerHTML = todos.map(todo => `
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 fade-in">
          <p class="text-sm font-medium text-white">${escHtml(todo.title)}</p>
          <p class="text-xs text-zinc-500 mt-0.5">${escHtml(todo.body)}</p>
          <p class="mono text-xs text-zinc-600 mt-2">${new Date(todo.created_at).toLocaleString()}</p>
        </div>
      `).join('')
    }

    async function handleCreateGuestTodo() {
      hideError('guest-create-error')
      const title = document.getElementById('guest-title').value.trim()
      const body  = document.getElementById('guest-body').value.trim()
      if (!title || !body) { showError('guest-create-error', 'Title and description are required.'); return }
      try {
        await apiFetch('/guest/todos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, body })
        })
        document.getElementById('guest-title').value = ''
        document.getElementById('guest-body').value  = ''
        await loadGuestTodos()
      } catch (err) { showError('guest-create-error', err.message) }
    }

    // ── UTILS ─────────────────────────────────────────────────────────
    function escHtml(str) {
      return String(str)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
    }

    // ── BOOT ──────────────────────────────────────────────────────────
    async function init() {
      if (getToken()) {
        try {
          const user = await apiFetch('/auth/me', { headers: authHeaders() })
          setUser(user)
        } catch (_) {
          clearToken(); clearUser()
        }
      }
      renderNav()
      if (getToken()) {
        showView('todos')
      } else {
        showView('auth')
        switchTab('login')
      }
    }

    init()
