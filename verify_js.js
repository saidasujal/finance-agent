const fs = require('fs');
const vm = require('vm');

function verifyJS(filepath) {
  try {
    const html = fs.readFileSync(filepath, 'utf8');
    
    // Find all content between <script> and </script>
    const scriptRegex = /<script[^>]*>([\s\S]*?)<\/script>/gi;
    let match;
    let count = 0;
    
    while ((match = scriptRegex.exec(html)) !== null) {
      count++;
      const jsCode = match[1];
      
      // Attempt to compile the script to check for syntax errors
      try {
        new vm.Script(jsCode);
        console.log(`PASS: Script block ${count} is syntactically valid.`);
      } catch (err) {
        console.error(`FAIL: Syntax error in script block ${count}:`, err.message);
        
        // Let's print the line number of the syntax error
        const stackLines = err.stack.split('\n');
        console.error(stackLines.slice(0, 5).join('\n'));
        process.exit(1);
      }
    }
    
    if (count === 0) {
      console.error("FAIL: No <script> blocks found in index.html!");
      process.exit(1);
    }
    
    console.log("All Javascript blocks validated successfully!");
  } catch (err) {
    console.error("Error reading file:", err.message);
    process.exit(1);
  }
}

verifyJS('/Users/sujal/finance-agent/index.html');
