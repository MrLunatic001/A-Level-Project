 # Shaders

vertex_src = """
# version 410
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_color;
layout(location = 3) in vec3 a_offset;
layout(location = 4) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
uniform mat4 light;


out vec3 v_color;
out vec2 v_texture;
out vec3 v_normal;

void main()
{
    vec3 final_pos = a_position + a_offset;
    gl_Position = projection * view * model * vec4(final_pos, 1.0);
    v_texture = a_texture;
    v_color = a_color;
    v_normal = (light * vec4(a_normal, 0.04f)).xyz;
}
"""

fragment_src = """
# version 410
in vec2 v_texture;
in vec3 v_normal;

out vec4 out_color;

uniform int switcher;
uniform ivec3 icolor;
uniform sampler2D s_texture;

void main()
    {
        if(switcher == 0){
            out_color = texture(s_texture, v_texture);
        }else{
            out_color = vec4(icolor.r/255.0, icolor.g/255.0, icolor.b/255.0, 1.0);
            }
        
    
    }
"""


"""
    
    
    vec3 ambientLightIntensity = vec3(0.3f, 0.2f, 0.4f);
        vec3 sunLightIntensity = vec3(0.9f, 0.9f, 0.9f);
        vec3 sunLightDirection = normalize(vec3(0.0f, 8.0f, 15.0f));
        vec4 texel = texture(s_texture, v_texture);
        vec3 lightIntensity = ambientLightIntensity + sunLightIntensity * max(dot(v_normal, sunLightDirection), 0.0f);
        if (switcher == 0){
            out_color = vec4(texel.rgb * lightIntensity, texel.a);
        }
        else{
            out_color = vec4(icolor.r/255.0, icolor.g/255.0, icolor.b/255.0, 1.0);   
        }
            
            
    
        
        
    
    
"""