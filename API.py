<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .search-box {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }

        .search-form {
            display: flex;
            gap: 10px;
        }

        .search-input {
            flex: 1;
            padding: 15px;
            border: 2px solid #667eea;
            border-radius: 10px;
            font-size: 16px;
        }

        .search-input:focus {
            outline: none;
            border-color: #764ba2;
        }

        .search-btn {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .search-btn:hover {
            transform: scale(1.05);
        }

        .search-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .current-weather {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            display: none;
        }

        .weather-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 20px;
        }

        .location {
            font-size: 2em;
            color: #333;
        }

        .weather-icon {
            width: 100px;
            height: 100px;
        }

        .weather-main {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .weather-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }

        .weather-card h3 {
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }

        .weather-card p {
            font-size: 2em;
            font-weight: bold;
        }

        .charts-container {
            display: grid;
            gap: 20px;
        }

        .chart-box {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .loading {
            text-align: center;
            color: white;
            font-size: 1.5em;
            display: none;
            margin: 20px 0;
        }

        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid white;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: 10px;
            vertical-align: middle;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .error {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            display: none;
            margin-bottom: 20px;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2em;
            }

            .location {
                font-size: 1.5em;
            }

            .search-form {
                flex-direction: column;
            }

            .weather-main {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌤️ Weather Dashboard</h1>
            <p>Real-time weather data and forecasts</p>
        </div>

        <div class="search-box">
            <div class="search-form">
                <input type="text" id="cityInput" class="search-input" placeholder="Enter city name (e.g., London, New York, Tokyo)">
                <button class="search-btn" id="searchBtn" onclick="getWeather()">Search</button>
            </div>
        </div>

        <div class="error" id="errorMsg"></div>
        <div class="loading" id="loading">Loading weather data</div>

        <div class="current-weather" id="currentWeather">
            <div class="weather-header">
                <div>
                    <div class="location" id="location"></div>
                    <div id="description" style="font-size: 1.2em; color: #666;"></div>
                </div>
                <img id="weatherIcon" class="weather-icon" src="" alt="Weather icon">
            </div>

            <div class="weather-main">
                <div class="weather-card">
                    <h3>Temperature</h3>
                    <p id="temperature"></p>
                </div>
                <div class="weather-card">
                    <h3>Feels Like</h3>
                    <p id="feelsLike"></p>
                </div>
                <div class="weather-card">
                    <h3>Humidity</h3>
                    <p id="humidity"></p>
                </div>
                <div class="weather-card">
                    <h3>Wind Speed</h3>
                    <p id="windSpeed"></p>
                </div>
            </div>
        </div>

        <div class="charts-container" id="chartsContainer" style="display: none;">
            <div class="chart-box" id="tempChart"></div>
            <div class="chart-box" id="humidityChart"></div>
            <div class="chart-box" id="conditionsChart"></div>
        </div>
    </div>

    <script>
        // Allow search on Enter key
        document.getElementById('cityInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                getWeather();
            }
        });

        async function getWeather() {
            const city = document.getElementById('cityInput').value.trim();
            const searchBtn = document.getElementById('searchBtn');
            
            if (!city) {
                showError('Please enter a city name');
                return;
            }

            // Show loading, hide previous data
            document.getElementById('loading').style.display = 'block';
            document.getElementById('currentWeather').style.display = 'none';
            document.getElementById('chartsContainer').style.display = 'none';
            document.getElementById('errorMsg').style.display = 'none';
            searchBtn.disabled = true;

            try {
                const response = await fetch(`/weather/${encodeURIComponent(city)}`);
                
                if (!response.ok) {
                    throw new Error('City not found');
                }

                const data = await response.json();
                displayWeather(data);
                
            } catch (error) {
                showError('City not found. Please check the spelling and try again.');
            } finally {
                document.getElementById('loading').style.display = 'none';
                searchBtn.disabled = false;
            }
        }

        function displayWeather(data) {
            const current = data.current;
            
            // Update current weather
            document.getElementById('location').textContent = `${current.city}, ${current.country}`;
            document.getElementById('description').textContent = current.description;
            document.getElementById('temperature').textContent = `${current.temperature}°C`;
            document.getElementById('feelsLike').textContent = `${current.feels_like}°C`;
            document.getElementById('humidity').textContent = `${current.humidity}%`;
            document.getElementById('windSpeed').textContent = `${current.wind_speed} m/s`;
            document.getElementById('weatherIcon').src = `https://openweathermap.org/img/wn/${current.icon}@2x.png`;
            
            // Update charts
            document.getElementById('tempChart').innerHTML = data.charts.temperature;
            document.getElementById('humidityChart').innerHTML = data.charts.humidity;
            document.getElementById('conditionsChart').innerHTML = data.charts.conditions;
            
            // Show data
            document.getElementById('currentWeather').style.display = 'block';
            document.getElementById('chartsContainer').style.display = 'grid';
        }

        function showError(message) {
            const errorDiv = document.getElementById('errorMsg');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        }

        // Load default city on page load
        window.onload = function() {
            document.getElementById('cityInput').value = 'London';
            getWeather();
        };
    </script>
</body>
</html>