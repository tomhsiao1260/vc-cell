import * as THREE from 'three'
import Loader from '../Loader'
import { VolumeMaterial } from './VolumeMaterial'
import { GenerateSDFMaterial } from './GenerateSDFMaterial'
import { FullScreenQuad } from 'three/examples/jsm/postprocessing/Pass'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import textureViridis from './textures/cm_viridis.png'

export default class ViewerCore {
  constructor({ meta, renderer, canvas }) {
    this.canvas = canvas
    this.renderer = renderer
    this.render = this.render.bind(this)

    this.meta = meta
    this.inverseBoundsMatrix = new THREE.Matrix4()
    this.volumePass = new FullScreenQuad(new VolumeMaterial())
    this.cube = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.5), new THREE.MeshBasicMaterial())
    this.cmtextures = { viridis: new THREE.TextureLoader().load(textureViridis) }

    this.params = {}
    this.params.surface = 0.05

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
    const label = await Loader.getTexture('inklabels.png')
    const volume = await Loader.getVolumeData('volume.nrrd')
    const sdf = await Loader.getVolumeData('sdf.nrrd')
    const u = await Loader.getVolumeData('u.nrrd')
    const v = await Loader.getVolumeData('v.nrrd')

    const { xLength: w, yLength: h, zLength: d } = volume
    const { xLength: sw, yLength: sh, zLength: sd } = sdf
    const { xLength: uvw, yLength: uvh, zLength: uvd } = u

    const matrix = new THREE.Matrix4()
    const center = new THREE.Vector3()
    const quat = new THREE.Quaternion()
    const scaling = new THREE.Vector3()
    const s = 1 / Math.max(w, h, d)

    scaling.set(w * s, h * s, d * s)
    matrix.compose(center, quat, scaling)
    this.inverseBoundsMatrix.copy(matrix).invert()

    const volumeTex = new THREE.Data3DTexture(volume.data, w, h, d)
    volumeTex.format = THREE.RedFormat
    volumeTex.type = THREE.UnsignedByteType
    volumeTex.minFilter = THREE.LinearFilter
    volumeTex.magFilter = THREE.LinearFilter
    volumeTex.needsUpdate = true

    const sdfTex = new THREE.Data3DTexture(sdf.data, sw, sh, sd)
    sdfTex.format = THREE.RedFormat
    sdfTex.type = THREE.UnsignedByteType
    sdfTex.minFilter = THREE.LinearFilter
    sdfTex.magFilter = THREE.LinearFilter
    sdfTex.needsUpdate = true

    const uTex = new THREE.Data3DTexture(u.data, uvw, uvh, uvd)
    uTex.format = THREE.RedFormat
    uTex.type = THREE.UnsignedByteType
    uTex.minFilter = THREE.LinearFilter
    uTex.magFilter = THREE.LinearFilter
    uTex.needsUpdate = true

    const vTex = new THREE.Data3DTexture(v.data, uvw, uvh, uvd)
    vTex.format = THREE.RedFormat
    vTex.type = THREE.UnsignedByteType
    vTex.minFilter = THREE.LinearFilter
    vTex.magFilter = THREE.LinearFilter
    vTex.needsUpdate = true

    // const

    this.volumePass.material.uniforms.label.value = label
    this.volumePass.material.uniforms.sdfTex.value = sdfTex
    this.volumePass.material.uniforms.volumeTex.value = volumeTex
    this.volumePass.material.uniforms.uTex.value = uTex
    this.volumePass.material.uniforms.vTex.value = vTex
    this.volumePass.material.uniforms.size.value.set(w, h, d)
    this.volumePass.material.uniforms.cmdata.value = this.cmtextures.viridis

    this.render()
  }

  render() {
    if (!this.renderer) return

    // this.renderer.render(this.scene, this.camera)

    this.volumePass.material.uniforms.surface.value = this.params.surface

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
