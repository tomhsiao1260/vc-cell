import * as THREE from 'three'
import Loader from '../Loader'
import { VolumeMaterial } from './VolumeMaterial'
import { GenerateSDFMaterial } from './GenerateSDFMaterial'
import { FullScreenQuad } from 'three/examples/jsm/postprocessing/Pass'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import textureViridis from './textures/cm_viridis.png'
import { TIFFLoader } from 'three/addons/loaders/TIFFLoader.js'

export default class ViewerCore {
  constructor({ meta, renderer, canvas }) {
    this.canvas = canvas
    this.renderer = renderer
    this.render = this.render.bind(this)

    this.meta = meta
    this.inverseBoundsMatrix = new THREE.Matrix4()
    this.volumePass = new FullScreenQuad(new VolumeMaterial())
    this.cube = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.5), new THREE.MeshBasicMaterial())
    this.cmtextures = { viridis: new THREE.TextureLoader().load(textureViridis, this.render) }

    this.init()
  }

  async init() {
    // scene setup
    this.scene = new THREE.Scene()
    this.scene.add(this.cube)

    // camera setup
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 50)
    this.camera.position.copy(new THREE.Vector3(0, 0, -1).multiplyScalar(1.0))
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
    const sdf = await Loader.getVolumeData('sdf.nrrd')
    const volume = await Loader.getVolumeData('volume.nrrd')
    const { xLength: w, yLength: h, zLength: d } = volume

    const matrix = new THREE.Matrix4()
    const center = new THREE.Vector3()
    const quat = new THREE.Quaternion()
    const scaling = new THREE.Vector3()
    const s = 1 / Math.max(w, h, d)

    scaling.set(w * s, h * s, d * s)
    matrix.compose(center, quat, scaling)
    this.inverseBoundsMatrix.copy(matrix).invert()

    const sdfTex = new THREE.Data3DTexture(volume.data, w, h, d)
    sdfTex.format = THREE.RedFormat
    // sdfTex.type = THREE.FloatType
    sdfTex.type = THREE.UnsignedByteType
    sdfTex.minFilter = THREE.LinearFilter
    sdfTex.magFilter = THREE.LinearFilter
    sdfTex.unpackAlignment = 1
    sdfTex.needsUpdate = true

    this.volumePass.material.uniforms.sdfTex.value = sdfTex
    this.volumePass.material.uniforms.size.value.set(volume.xLength, volume.yLength, volume.zLength)

    this.render()
  }

  render() {
    if (!this.renderer) return

    // this.renderer.render(this.scene, this.camera)

    this.camera.updateMatrixWorld()
    this.volumePass.material.uniforms.projectionInverse.value.copy(this.camera.projectionMatrixInverse)
    this.volumePass.material.uniforms.sdfTransformInverse.value
      .copy(new THREE.Matrix4())
      .invert()
      .premultiply(this.inverseBoundsMatrix)
      .multiply(this.camera.matrixWorld)

    this.volumePass.render(this.renderer)
  }
}
