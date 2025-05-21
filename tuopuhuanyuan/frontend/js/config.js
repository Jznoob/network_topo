document.addEventListener('DOMContentLoaded', function() {
    const editor = CodeMirror.fromTextArea(document.getElementById("configEditor"), {
        mode: "javascript",
        theme: "monokai",
        lineNumbers: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        indentUnit: 4
    });

    document.getElementById('configType').addEventListener('change', function(e) {
        editor.setOption("mode", e.target.value);
    });

    document.getElementById('configFile').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                editor.setValue(e.target.result);
            };
            reader.readAsText(file);
        }
    });

    document.getElementById('generateTopology').addEventListener('click', function() {
        window.location.href = 'topology.html';
    });
}); 