const world = Globe()

// Globe basic settings
world.globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
world.backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
world(document.getElementById('globe_scene'));

// Custom globe material
const globeMaterial = world.globeMaterial();
globeMaterial.bumpScale = 10;

new THREE.TextureLoader().load('//unpkg.com/three-globe/example/img/earth-water.png', texture => {
    globeMaterial.specularMap = texture;
    globeMaterial.specular = new THREE.Color('grey');
    globeMaterial.shininess = 15;
});

const directionalLight = world.lights().find(light => light.type === 'DirectionalLight');
directionalLight && directionalLight.position.set(1, 1, 1); // change light position to see the specularMap's effect
