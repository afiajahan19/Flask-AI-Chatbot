const fs = require('fs');

// Create or overwrite a file in the current directory
fs.writeFileSync('example.txt', 'Hello File System!');

// Read and print the file content
const data = fs.readFileSync('example.txt', 'utf8');
console.log(data);
