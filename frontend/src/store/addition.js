import store from "@/store"

export default class UserSetting {
  constructor(key, defaultValue=null) {
    this._key = key
    this._value = defaultValue
    this._defaultValue = defaultValue
  }

  get value() {
    const individualName = this.genVarNameForLocalstorage()
    if(individualName) {
      let lsValue = JSON.parse(localStorage.getItem(individualName))
      lsValue !== null ? this._value = lsValue : this.value = this._defaultValue
    }
    return this._value
  }

  set value(newValue) {
    this._value = newValue
    localStorage.setItem(this.genVarNameForLocalstorage(), JSON.stringify(this._value))
  }

  removeFromLocalstorage() {
    localStorage.removeItem(this.genVarNameForLocalstorage())
  }

  switch(newValue) {
    let findValueIndex = this._value.findIndex(v => v === newValue)
    findValueIndex === -1 ? this._value.push(newValue) : this._value.splice(findValueIndex, 1)
    localStorage.setItem(this.genVarNameForLocalstorage(), JSON.stringify(this._value))
  }

  genVarNameForLocalstorage() {
    if(store && store.getters.userInformation) {
      return JSON.stringify({identifier: store.getters.userInformation.username, key: this._key})
    }
    else return null
  }
}