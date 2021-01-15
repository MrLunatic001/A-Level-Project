# Shaders

vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_color;
layout(location = 3) in vec3 a_offset;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;


out vec3 v_color;
out vec2 v_texture;

void main()
{
    vec3 final_pos = a_position + a_offset;
    gl_Position = projection * view * model * vec4(final_pos, 1.0);
    v_texture = a_texture;
    v_color = a_color;
}
"""

fragment_src = """
# version 330
in vec2 v_texture;

out vec4 out_color;

uniform int switcher;
uniform ivec3 icolor;
uniform sampler2D s_texture;

void main()
{
    if (switcher == 0){
        out_color = texture(s_texture, v_texture);
    }
    else if (switcher == 1){
        out_color = vec4(icolor.r/255.0, icolor.g/255.0, icolor.b/255.0, 1.0);   
    }
}
"""