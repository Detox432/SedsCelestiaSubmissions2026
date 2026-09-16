#version 430

layout(local_size_x = 64) in;

layout(rgba32f, binding = 0) uniform image2D out_image;

struct Segment {
    vec2 a;
    vec2 b;
    int mat;
    int _pad;
};

layout(std430, binding = 1) buffer SegmentBuffer {
    Segment segments[];
};

uniform int seg_count;
uniform int num_rays;
uniform vec2 light_pos;
uniform float width;
uniform float height;

float ray_intersect(vec2 O, vec2 D, vec2 A, vec2 B){
    float z1 = D.y*(A.x - O.x) - D.x*(A.y - O.y);
    float z2 = D.y*(B.x - O.x) - D.x*(B.y - O.y);
    if (z1*z2 > 0.0)
        return 0.0;
    if (abs(z1 - z2) < 0.000001){
    return 0.0;
}
    float projection_A = (A.x - O.x)*D.x + (A.y - O.y)*D.y;
    float projection_B = (B.x - O.x)*D.x + (B.y - O.y)*D.y;
    if (projection_A < 0.0 && projection_B < 0.0)
        return 0.0;

    float t = projection_A + (projection_B - projection_A) * (z1 / (z1 - z2));
    return t;
}

void draw_line(vec2 p0, vec2 p1, vec4 base_color, float accumulated_dist) {
    vec2 diff = p1 - p0;
    float len = length(diff);
    int steps = int(len) + 1;
    
    for (int i = 0; i <= steps; i++) {
        float t = float(i) / float(steps);
        vec2 p = p0 + diff * t;
        
        float current_dist = accumulated_dist + (len * t);
        
        float attenuation = 1.0 / (1.0 + 0.002 * current_dist + 0.00001 * current_dist * current_dist);
        
        ivec2 coord = ivec2(int(p.x), int(p.y));
        if (coord.x >= 0 && coord.x < int(width) && coord.y >= 0 && coord.y < int(height)) {
            vec4 existing = imageLoad(out_image, coord);
            imageStore(out_image, coord, existing + (base_color * attenuation));
        }
    }
}

void main(){
    uint ray_id = gl_GlobalInvocationID.x;
    if (ray_id < seg_count) {
        vec4 line_color = (segments[ray_id].mat == 1) ? vec4(0.0, 1.0, 0.0, 1.0) : vec4(0.0, 0.5, 1.0, 1.0);
        draw_line(segments[ray_id].a, segments[ray_id].b, line_color, 0.0);
    }
    float angle = 2.0 * 3.14159265 * float(ray_id) / float(num_rays);
    vec2 origin = light_pos;
    vec2 direction = vec2(cos(angle), sin(angle));
    
    vec4 color = vec4(1.0, 1.0, 1.0, 0.0);
    
    float accumulated_dist = 0.0;

    for (int bounce = 0; bounce < 8; bounce++) {
        float closest_t = 1e9;
        int closest_i = -1;

        for (int i = 0; i < seg_count; i++) {
            float t = ray_intersect(origin, direction, segments[i].a, segments[i].b);
            if (t > 0.0 && t < closest_t) {
                closest_t = t;
                closest_i = i;
            }
        }

        if (closest_i == -1) break;

        vec2 hit = origin + direction * closest_t;
        
        draw_line(origin, hit, color * 0.1, accumulated_dist);
        
        accumulated_dist += closest_t;

        if (segments[closest_i].mat == 0) break;

        vec2 n = normalize(vec2(-(segments[closest_i].b.y - segments[closest_i].a.y), segments[closest_i].b.x - segments[closest_i].a.x));
        if (dot(n, direction) > 0.0) n = -n;
        direction = reflect(direction, n);
        origin = hit + direction * 0.001;
        
        color *= 0.8; 
    }
}

