const globe = Globe()

// Basic globe settings
globe(document.getElementById('globe_scene'));
globe.globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
globe.backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')

// Custom globe material
const globeMaterial = globe.globeMaterial();
globeMaterial.bumpScale = 10;

new THREE.TextureLoader().load('//unpkg.com/three-globe/example/img/earth-water.png', texture => {
    globeMaterial.specularMap = texture;
    globeMaterial.specular = new THREE.Color('grey');
    globeMaterial.shininess = 15;
});

const directionalLight = globe.lights().find(light => light.type === 'DirectionalLight');
directionalLight && directionalLight.position.set(1, 1, 1); // change light position to see the specularMap's effect

let points = []

function settings_data() {
    const settings = document.getElementById("settings_modal")

    $('#settings_form').submit(function (event) {
        event.preventDefault()
        settings.style.display = "none"

        $.ajax({
            url: '/settings-data',
            data: $('#settings_form').serialize(),
            type: 'POST',
            success: function(response){
                points = ([
                    {
                        name: response[0][1],
                        lat: response[0][2],
                        lng: response[0][3],
                        color: 'red'
                    }])

                globe
                    .pointsData(points)
                    .pointLabel('name')
                    .pointColor('color')
                    .pointRadius(0.2)

                $("#proximity").text("Click On The Globe To Move")
                $("#current").text("AT: " + response[0][1])
                $("#attempts").text("ATTEMPTS: " + 0)
                $("#distance").text("DISTANCE: " + 0 + " KM")
                $("#target").text("TO: " + response[1][1])

                document.querySelectorAll(".ui-labels").forEach(function(element) {
                    element.style.display = "block"
                });
            },
            error: function(error){
                console.log("Could not retrieve starter or target")
            }
        });
    })
}

function game_navigation(lat, lng) {
    $.ajax({
        url: '/navigation-data',
        data: JSON.stringify({ 'lat': lat, 'lng': lng }),
        type: 'POST',
        contentType: 'application/json',
        success: function(response){
            let new_point
            let place = $("#proximity")

            $("#current").text("AT: " + response[0][1])
            $("#attempts").text("ATTEMPTS: " + response[1])
            $("#distance").text("DISTANCE: " + response[2] + " KM")

            if (!response[3]) {
                new_point = {
                    name: response[0][1],
                    lat: response[0][2],
                    lng: response[0][3],
                    color: 'blue'
                }

                switch (response[4]) {
                    case 0:
                        place.text("You are closer to the target")
                        break
                    case 1:
                        place.text("You are farther to the target")
                        break
                    case 2:
                        place.text("You are at the same distance")
                        break
                }
            } else {
                new_point = {
                    name: response[0][1],
                    lat: response[0][2],
                    lng: response[0][3],
                    color: 'green'
                }

                points.push(new_point)
                globe.pointsData(points)

                setTimeout(function () {
                    alert("You have won the game! It took you " + response[1] + " attempts.")
                    window.location.reload()
                }, 1000)
            }

            points.push(new_point)
            globe.pointsData(points)
        },
        error: function(error){
            console.log("Could not retrieve airport data")
        }
    });
}

window.onload = function () {
    settings_data()
}

globe.onGlobeClick(({ lat, lng }) => {
    game_navigation(lat, lng);
});