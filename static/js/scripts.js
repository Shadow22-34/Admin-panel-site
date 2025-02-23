document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('editor')) {
        var editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
            mode: 'lua',
            theme: 'monokai',
            lineNumbers: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            indentUnit: 4,
            tabSize: 4,
            lineWrapping: true,
            extraKeys: {
                "Tab": function(cm) {
                    cm.replaceSelection("    ", "end");
                }
            }
        });
    }

    // Script viewing functionality
    function viewScript(scriptId) {
        const modal = document.createElement('div');
        modal.className = 'script-modal';
        
        fetch(`/script/${scriptId}`)
            .then(response => response.json())
            .then(data => {
                modal.innerHTML = `
                    <div class="script-modal-content">
                        <div class="script-modal-header">
                            <h2>${data.name}</h2>
                            <span class="close-modal">&times;</span>
                        </div>
                        <div class="script-modal-body">
                            <pre><code class="lua">${data.content}</code></pre>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
                
                modal.querySelector('.close-modal').onclick = () => {
                    modal.remove();
                };
            });
    }

    // Add click handlers to view buttons
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.onclick = () => viewScript(btn.dataset.scriptId);
    });

    // Real-time stats update
    function updateStats() {
        fetch('/stats')
            .then(response => response.json())
            .then(data => {
                document.querySelector('.total-buyers').textContent = data.total_buyers;
                document.querySelector('.active-users').textContent = data.active_users;
                document.querySelector('.total-executions').textContent = data.total_executions;
            });
    }

    // Update stats every 30 seconds
    setInterval(updateStats, 30000);
});