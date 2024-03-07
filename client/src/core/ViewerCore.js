import * as THREE from 'three'
import { VolumeMaterial } from './VolumeMaterial'
import { GenerateSDFMaterial } from './GenerateSDFMaterial'
import { FullScreenQuad } from 'three/examples/jsm/postprocessing/Pass'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import textureViridis from './textures/cm_viridis.png'

export default class ViewerCore {
  constructor(meta) {
    this.meta = meta
    this.render = this.render.bind(this)
    this.canvas = document.querySelector('.webgl')
    this.volumePass = new FullScreenQuad(new VolumeMaterial())
    this.cube = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.5), new THREE.MeshBasicMaterial())
    this.cmtextures = { viridis: new THREE.TextureLoader().load(textureViridis, this.render) }

    this.init()
  }

  init() {
    // renderer setup
    this.renderer = new THREE.WebGLRenderer({ antialias: true, canvas: this.canvas })
    this.renderer.setPixelRatio(window.devicePixelRatio)
    this.renderer.setSize(window.innerWidth, window.innerHeight)
    this.renderer.setClearColor(0, 0)
    this.renderer.outputColorSpace = THREE.SRGBColorSpace

    // scene setup
    this.scene = new THREE.Scene()
    this.scene.add(this.cube)

    // camera setup
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 50)
    this.camera.position.copy(new THREE.Vector3(0, 0, 1).multiplyScalar(1.0))
    this.camera.up.set(0, -1, 0)
    this.camera.far = 5
    this.camera.updateProjectionMatrix()

    window.addEventListener(
      'resize',
      () => {
        this.camera.aspect = window.innerWidth / window.innerHeight
        this.camera.updateProjectionMatrix()
        this.renderer.setSize(window.innerWidth, window.innerHeight)
        this.render()
      },
      false
    )

    const controls = new OrbitControls(this.camera, this.canvas)
    controls.addEventListener('change', this.render)

    this.cmtextures.viridis.minFilter = THREE.NearestFilter
    this.cmtextures.viridis.maxFilter = THREE.NearestFilter
    this.volumePass.material.uniforms.cmdata.value = this.cmtextures.viridis

    this.sdfTexGenerate()
  }

  async sdfTexGenerate() {
    const r = 1.0
    const w = 186
    const h = 149
    const d = 126

    const sdfTex = new THREE.WebGL3DRenderTarget(w * r, h * r, d * r)
    sdfTex.texture.format = THREE.RedFormat
    // sdfTex.texture.format = THREE.RGFormat
    sdfTex.texture.type = THREE.FloatType
    sdfTex.texture.minFilter = THREE.LinearFilter
    sdfTex.texture.magFilter = THREE.LinearFilter

    const generateSdfPass = new FullScreenQuad(new GenerateSDFMaterial())

    for (let i = 0; i < d * r; i++) {
      const texture = await new THREE.TextureLoader().loadAsync(`20230702185753/${i + 935}.png`)
      texture.minFilter = THREE.NearestFilter
      texture.magFilter = THREE.NearestFilter

      this.renderer.setRenderTarget(sdfTex, i)
      generateSdfPass.material.uniforms.sliceData.value = texture
      generateSdfPass.render(this.renderer)
    }
    this.renderer.setRenderTarget(null)
    generateSdfPass.material.dispose()

    this.volumePass.material.uniforms.sdfTex.value = sdfTex.texture
    this.render()
  }

  render() {
    if (!this.renderer) return

    // this.renderer.render(this.scene, this.camera)
    this.volumePass.render(this.renderer)
  }
}
