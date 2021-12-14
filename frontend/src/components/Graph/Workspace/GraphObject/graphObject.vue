<template>
  <g
    @mousedown.capture="$emit('selectObject', object)"
    @mouseup.ctrl="$emit('setChoosingObject', object.id)"
    @mouseup.alt="$emit('setRelatedObjects', object)"
    @wheel.stop="scroll"
    @click.stop=""
  >
    <node ref="node" :data="object">
      <body-object :object="object" :class="objectClass"/>
    </node>
  </g>
</template>

<script>
import Node from '@/components/Graph/lib/components/Node'
import BodyObject from "@/components/Graph/Workspace/GraphObject/bodyObject"

export default {
  name: "graphObject",
  components: {BodyObject, Node},
  props: {
    object: Object,
    choosing: Boolean,
  },
  computed: {
    objectClass: function () {
      return this.choosing ? 'choosing-object' : 'body-object'
    }
  },
  methods: {
    scroll(event) {
      if(event.deltaY > 0 && this.object.size / 1.5 > 300){
        this.object.x += (((this.object.size/3) - (this.object.size/3)/1.5))/2
        this.object.y += (((this.object.size/3) - (this.object.size/3)/1.5))/2
        this.object.size /= 1.5
      }
      if (event.deltaY < 0 && this.object.size * 1.5 < 1500){
        this.object.x -= (((this.object.size/3)*1.5 - (this.object.size/3)))/2
        this.object.y -= (((this.object.size/3)*1.5 - (this.object.size/3)))/2
        this.object.size *= 1.5
      }
      this.$nextTick(() => {
        this.updateNode()
      })
    },
    updateNode() {
      // this.$refs.node.fitContent()
    },
  }
}
</script>

<style scoped>
.choosing-object {
  /*box-shadow: 0px 0px 20px 0px rgb(255 0 0 / 50%), 0px 0px 20px 20px rgb(255 0 0 / 40%), 0 0 18px 20px rgb(255 0 0 / 30%);*/
  /*transition: all 0.3s cubic-bezier(.25,.8,.25,1);*/
  animation: pulse-red 1s infinite;
}

@keyframes pulse-red {
  0% {
    box-shadow: 0 0 0 0 rgb(255 82 82 / 70%), 0 0 0 0 rgb(255 82 82 / 70%);
  }

  30% {
    box-shadow: 0 0 5px 5px rgb(255 82 82 / 70%), 0 0 0 0 rgb(255 82 82 / 70%);
  }

  50% {
    box-shadow: 0 0 10px 10px rgba(255, 82, 82, 0), 0 0 0 0 rgb(255 82 82 / 70%);
  }

  70% {
    box-shadow: 0 0 5px 5px rgb(255 82 82 / 70%), 0 0 0 0 rgb(255 82 82 / 70%);
  }

  100% {
    box-shadow: 0 0 5px 5px rgba(255, 82, 82, 0), 0 0 0 0 rgb(255 82 82 / 70%);
  }
}

.choosing-object:hover {
  box-shadow: 0 7px 8px -4px rgb(255 0 0 / 20%), 0 12px 17px 2px rgb(255 0 0 / 14%), 0 5px 22px 4px rgb(255 0 0 / 12%);
}
.body-object {
  box-shadow: 0 3px 5px -1px rgb(0 0 0 / 20%), 0 6px 10px 0 rgb(0 0 0 / 14%), 0 1px 18px 0 rgb(0 0 0 / 12%);
  transition: all 0.3s cubic-bezier(.25,.8,.25,1);
}
.body-object:hover {
  box-shadow: 0 7px 8px -4px rgb(0 0 0 / 20%), 0 12px 17px 2px rgb(0 0 0 / 14%), 0 5px 22px 4px rgb(0 0 0 / 12%);
}

</style>