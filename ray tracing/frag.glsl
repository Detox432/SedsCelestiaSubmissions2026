#version 430
in vec2 uv;
out vec4 out_color;
uniform sampler2D tex;
void main() {
    vec3 c = texture(tex, uv).rgb;
    c = c / (c + vec3(1.0));
    c = pow(c, vec3(1.0 / 2.2));
    out_color = vec4(c, 1.0);
}