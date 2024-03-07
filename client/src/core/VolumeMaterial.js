import { ShaderMaterial } from 'three'

export class VolumeMaterial extends ShaderMaterial {
  constructor(params) {
    super({
      defines: {},

      uniforms: {
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
        varying vec2 vUv;
        uniform sampler2D cmdata;

        void main() {
            // gl_FragColor = vec4(vUv, 1.0, 1.0);
            gl_FragColor = texture2D(cmdata, vUv);
        }
        `,
    })
  }
}
