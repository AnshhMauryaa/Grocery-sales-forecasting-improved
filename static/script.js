body {
    text-align: center;
    font-family: Arial, sans-serif;
    margin-top: 100px;
}

/* Spinner circle */
.loader {
    border: 10px solid #f3f3f3;
    border-top: 10px solid #3498db;
    border-radius: 50%;
    width: 80px;
    height: 80px;
    animation: spin 1s linear infinite;
    margin: auto;
}

/* Animation */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}