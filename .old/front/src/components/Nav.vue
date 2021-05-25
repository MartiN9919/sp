<template>
  <div class="nav">
    <div v-on:click="click_header" class="dd">жми сюда! {{ vv2 }} !!! {{ props.dat }} !!! </div>
    <span class="hn" :title="message">Hint</span><br>
    <span v-if="seen">Show</span><br>
    <input v-on:change="inp_reverce" v-model="vv"><br>
    <ol>
        <li v-for="txt_for_item in txt_for">
            {{ txt_for_item.text }}
        </li>
    </ol>
    <p>{{ vars }}</p>

  </div>
</template>


<script>
    export default {
        name: 'Nav',
        data: () => ({
            vv: 'Введи сюда',
            vv2 : '',
            props: {
                dat: 555,
            },
            message: 'df '+new Date().toLocaleString(),
            seen: true,
            txt_for: [
                { text: 'Изучить 1' },
                { text: 'Изучить 2' },
                { text: 'Создать 3' },
            ],
        }),

        props: [
            'vars',
        ],

        methods: {
            click_header: function() {
                console.log(this.data);
                this.txt_for.push({ text: 'Создать 4' });
            },
            inp_reverce: function(){
                this.vv2 = this.vv+'zzz';
            },
        },
    }
</script>

<style scoped lang="scss">
.dd {
    font-size: 3em;
}

.hn {
    font-size: 2em;
}

</style>
