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
                console.log(response)
                globe
                    .pointsData([
                        {
                            lat: response[0][2],
                            lng: response[0][3],
                            size: 1,
                            color: 'purple'
                        }
                    ])
                    .pointColor('color')
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
            console.log(response);
        },
        error: function(error){
            console.log("Could not retrieve airport data");
        }
    });
}

window.onload = function () {
    settings_data()
}

globe.onGlobeClick(({ lat, lng }) => {
    game_navigation(lat, lng);
});