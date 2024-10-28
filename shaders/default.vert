#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;

out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

/*
 * Vertex Shader
 * 
 * This shader is responsible for transforming vertex positions, normals, and texture coordinates
 * from model space to clip space. It also computes the fragment position and normal in world space.
 * 
 * Attributes:
 * - in_position: The position of the vertex in model space.
 * - in_texcoord_0: The texture coordinates of the vertex.
 * - in_normal: The normal vector of the vertex in model space.
 * 
 * Uniforms:
 * - m_model: The model matrix that transforms vertices from model space to world space.
 * - m_view: The view matrix that transforms vertices from world space to view space.
 * - m_proj: The projection matrix that transforms vertices from view space to clip space.
 * 
 * Varyings:
 * - uv_0: The texture coordinates passed to the fragment shader.
 * - fragPos: The position of the fragment in world space.
 * - normal: The normal vector of the fragment in world space.
 * 
 * Outputs:
 * - gl_Position: The position of the vertex in clip space.
 */
void main() {
    uv_0 = in_texcoord_0;
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}