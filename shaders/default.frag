#version 330 core



/*

    This fragment shader is responsible for calculating the final color of each pixel.

    Outputs:
    - fragColor: The final color output of the fragment shader.

    Inputs:
    - uv_0: The texture coordinates for the fragment.
    - normal: The normal vector at the fragment position.
    - fragPos: The position of the fragment in world space.

    Structures:
    - Light: A structure representing a light source with the following properties:
        - position: The position of the light source.
        - Ia: Ambient light intensity.
        - Id: Diffuse light intensity.
        - Is: Specular light intensity.

    Uniforms:
    - light: An instance of the Light structure representing the light source.
    - u_texture_0: A sampler for the texture to be applied to the fragment.
    - camPos: The position of the camera in world space.
*/
layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;


/**
 * Computes the lighting effect on a given color based on ambient, diffuse, and specular components.
 *
 * @param color The base color of the fragment.
 * @return The color of the fragment after applying lighting effects.
 *
 * The function uses the following global variables:
 * - vec3 normal: The normal vector at the fragment.
 * - vec3 fragPos: The position of the fragment.
 * - vec3 camPos: The position of the camera.
 * - struct light: A structure containing the light properties:
 *   - vec3 position: The position of the light source.
 *   - vec3 Ia: The ambient light intensity.
 *   - vec3 Id: The diffuse light intensity.
 *   - vec3 Is: The specular light intensity.
 */
vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);
    vec3 ambient = light.Ia;

    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = light.Id * diff;

    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = light.Is * spec;

    return color * (ambient + diffuse + specular);
}

/*
    Fragment shader for applying gamma correction and lighting effects.

    This shader performs the following operations:
    1. Applies gamma correction to the texture color.
    2. Applies lighting effects using the getLight function.
    3. Re-applies inverse gamma correction to the final color.
    
    Uniforms:
    - u_texture_0: The input texture.

    Inputs:
    - uv_0: The texture coordinates.

    Outputs:
    - fragColor: The final color output of the fragment shader.
*/
void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));

    color = getLight(color);

    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}