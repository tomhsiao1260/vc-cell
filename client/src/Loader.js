import { NRRDLoader } from 'three/examples/jsm/loaders/NRRDLoader'

export default class Loader {
  constructor() {}

  static getMeta() {
    return fetch('meta.json').then((res) => res.json())
  }

  static getVolumeData(filename) {
    return new NRRDLoader().loadAsync(filename)
  }
}
