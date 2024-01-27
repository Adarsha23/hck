// Adarsha Prasai
// student id 2408599
// Event handling

// Adding an event listener for search button
document.querySelector("#mybutton").addEventListener("click", () => {
//    Retrieves the data of the city we searched
    retrieve(document.querySelector("#search-input").value);
});

// Adding an event listener to the element with the id "search-input" for a keydown event
document.querySelector("#search-input").addEventListener("keydown", (event) => {
    // Checking if "Enter" is pressed"
    if (event.key === "Enter") {
        //retrieving weather data from the API according to search input"
        retrieve(document.querySelector("#search-input").value);
    }
});

// Main function
// using async function to retrieve info of a city while the default city is hinganghat
async function retrieve(city = "Hinganghat") {
    
    // in try code will be executed and if error occurs, they will be caught and handled in 'catch'
    try {
        //  this is OpenWeatherMap API key
        const apiKey = "191111594aefbbc3fc785a64be8d0e63";

        // Fetching weather data from OpenWeatherMap API if provided city and API key
        const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&APPID=${apiKey}`);
        
        // Parsing the response as JSON await is used to wait for the parsing to be completed
        const data = await response.json();
        // logs parsed JSON to console
        console.log(data);

        // MANIPULATING the DOM based on the retrieved weather data
        // selects ID of the required fields and capitalized is used to make the first letter capital 
        document.querySelector("#cityname").textContent = capitalize(city);
        document.querySelector("#Weathertype").textContent = capitalize(data["weather"][0].description);
        document.querySelector("#displaytemp").textContent = String(Math.round(data["main"].temp - 273.15)) + "°C";
        document.querySelector("#displaywin").textContent = String(data["wind"].speed) + "km/h";
        document.querySelector("#displayhum").textContent = String(data["main"].humidity) + "%";
        document.querySelector("#displayair").textContent = String(data["main"].pressure) + "mbar";
        document.querySelector("img").src = `https://openweathermap.org/img/wn/${data["weather"][0].icon}@2x.png`;

    } catch (err) {
        // logs errors to console 
        console.error(err);
    }
}

// Function to make the first letter of each word capital in a string
function capitalize(str) {
    // splits the input string into array of words
    myArr = str.split(" ");

    // array to store new capital words
    newArr = [];

    //  iterates through each word, Capitalizing the first letter of each word using touppercase()and pushing them to a new array
    myArr.forEach(value => {
        newArr.push(value[0].toUpperCase() + value.slice(1));
    });
    
    // Joining the array of capitalized words into a string
    return newArr.join(" ");
}

// using default city hinganghat  to fetch and show weather info
retrieve();

