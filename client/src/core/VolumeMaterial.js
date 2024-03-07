import { ShaderMaterial, Matrix4, Vector2, Vector3 } from 'three'

export class VolumeMaterial extends ShaderMaterial {
  constructor(params) {
    super({
      defines: {},

      uniforms: {
        sdfTex: { value: null },
        cmdata: { value: null },
      },

      vertexShader: /* glsl */ `
        varying vec2 vUv;

        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
        }
        `,

      fragmentShader: /* glsl */ `
        precision highp sampler3D;

        varying vec2 vUv;
        uniform sampler2D cmdata;
        uniform sampler3D sdfTex;

        void main() {
          float fragCoordZ = -1.;

          float v = texture2D(sdfTex, vec3(vUv, 1.0)).r;
          gl_FragColor = vec4(v, v, v, 1.0);
          return;
        }
        `,
    })
  }
}
