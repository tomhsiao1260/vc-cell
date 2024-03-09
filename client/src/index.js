import * as THREE from 'three'
import ViewerCore from './core/ViewerCore'
import Loader from './Loader'

init()

async function init() {
  // renderer setup
  const canvas = document.querySelector('.webgl')
  const renderer = new THREE.WebGLRenderer({ antialias: true, canvas: canvas })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setClearColor(0, 0)
  renderer.outputColorSpace = THREE.SRGBColorSpace

  const meta = await Loader.getMeta()
  const viewer = new ViewerCore({ meta, renderer, canvas })
  update(viewer)
}

function update(viewer) {
  viewer.render()
}
