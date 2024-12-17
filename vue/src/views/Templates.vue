<script setup>
    import { ref } from 'vue'

    import Content from '@/components/Content.vue'

    import IconAlignLeft from '@/components/icons/IconAlignLeft.vue';
    import IconTable from '@/components/icons/IconTable.vue';

    const sampleData = ref([
        {
            name: "Stephen Curry",
            age: 25,
            height: 174,
            location: "Los Angeles, CA"
        },
        {
            name: "Klay Thompson",
            age: 27,
            height: 181,
            location: "Akron, OH"
        }
    ])

    function addDataSample()
    {
        sampleData.value.push(newDataSample.value)
        newDataSample.value = {}
    }

    const newDataSample = ref({})
    const selectedData = ref({})

    function clickItem(obj)
    {
        selectedData.value = obj
        console.log(selectedData.value)
        console.log("Clicked item: " + sampleData.value.findIndex(x => x == obj))
    }

    const rangeValue = ref(50)

    function deleteMessage(messageId)
    {
        const element = document.getElementById(messageId);
        if(element)
            element.remove();
    }

    // Event for setting header alert

    const emit = defineEmits(['onHeaderAlert'])
 
    const setHeaderAlert = (alert) => {
        emit('onHeaderAlert', "UI Templates", alert)
    }
    
    const newHeaderAlert = ref("")

</script>

<template>
    <h2>User-Interface Templates</h2>
    
    <!-- Paragraphs-->
    <Content>
        <template #icon>
            <IconAlignLeft />
        </template>
        <template #heading>Paragraffer</template>
        
        <span class="paragraph">
            Til paragraffer med overskrifter er lavet et Vue komponent, <code>@/components/Content.vue</code>.
            Komponentet benyttes med <code>&ltContent&gt</code> HTML tagget efter import, og inderholder et <code>#icon</code>,
            en <code>#heading</code>, og subtekst.
        </span>
        <span class="paragraph">
            Herudover findes klassen <code>paragraph</code> som kan tilknyttes eksempelvis <code>&lt;span&gt;</code>-elementer for at skabe naturlige afsnit i tekst og andet indhold.
        </span>
    </Content>

    <!-- Table -->
    <Content>
        <template #icon>
            <IconTable />
        </template>
        <template #heading>Dynamisk tabel</template>

        <span class="paragraph">
            Tabeller indsættes med almindeligt HTML, og kan laves dynamiske med Vue's <code>v-for</code>-tag. Tabeller kan også indsættes i kort hvortil de automatisk tilpasses.
        </span>
        
        <table>
            <thead>
                <tr>
                    <th v-for="key in Object.keys(sampleData[0])" class="capitalize">{{key}}</th>
                    <th></th>
                </tr>
            </thead>
            <tr v-for="obj in sampleData">
                <td v-for="key in Object.keys(sampleData[0])">{{obj[key]}}</td>
                <td><button @click="clickItem(obj)">Se mere</button></td>
            </tr>
        </table>
    </Content>

    <!-- Cards -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Kort</template>

        <span class="paragraph">Kort indsættes som <code>&lt;div&gt;</code>-elementer med klassen <code>card</code>, og kan indeholde en <code>header</code> og en <code>card-body</code>. Kortene kan farves med predefinerede farveklasser.</span>

        <div class="flexbox">
            
            <div class="card">
                <div class="header">
                    <span v-if="selectedData['name']">{{selectedData['name']}}</span>
                    <span v-else>Overskrift</span>
                </div>
                
                <div class="card-body">

                    <table v-if="selectedData">
                        <tr v-for="key in Object.keys(selectedData)">
                            <td class="capitalize heavy">{{key}}</td>
                            <td>{{selectedData[key]}}</td>
                        </tr>
                    </table>

                    <span>Tryk på en "Se mere"-knap fra den dynamiske tabel for at udfylde kortet.</span>

                </div>
            </div>

            <div class="card blue">
                <div class="header">
                    Overskrift
                </div>
                <div class="card-body">
                    Dette kort har klassen <code>blue</code>. Du kan også lave tekst i <code>&lt;span&gt;</code>-elementer <span class="blue">blå</span>.
                </div>
            </div>

            <div class="card green">
                <div class="header">
                    Overskrift
                </div>
                <div class="card-body">
                    Dette kort har klassen <code>green</code>. Du kan også lave tekst i <code>&lt;span&gt;</code>-elementer <span class="green">grøn</span>.
                </div>
            </div>

            <div class="card red">
                <div class="header">
                    Overskrift
                </div>
                <div class="card-body">
                    Dette kort har klassen <code>red</code>. Du kan også lave tekst i <code>&lt;span&gt;</code>-elementer <span class="red">rød</span>.
                </div>
            </div>

            <div class="card orange">
                <div class="header">
                    Overskrift
                </div>
                <div class="card-body">
                    Dette kort har klassen <code>orange</code>. Du kan også lave tekst i <code>&lt;span&gt;</code>-elementer <span class="orange">orange</span>.
                </div>
            </div>

            <div class="card randers">
                <div class="header">
                    Overskrift
                </div>
                <div class="card-body">
                    Dette kort har klassen <code>randers</code>. Du kan også lave tekst i <code>&lt;span&gt;</code>-elementer <span class="randers">Randers-blå</span>.
                </div>
            </div>


        </div><!-- /flexbox -->

    </Content>

    <!-- Forms -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Formular</template>

        <span class="paragraph">
            Formularer indsættes som almindelig HTML og kan gøres client-sided med Vue's <code>@submit.prevent</code>-tag.
            Formularen herunder er ligeledes bygget dynamisk med <code>v-for</code>-tag på objektets keys.
        </span>
        
        <form @submit.prevent="addDataSample">
            <fieldset>
                <div class="flexbox">
                    <div v-for="key in Object.keys(sampleData[0])">
                        <label :for="key" class="capitalize">{{key}}</label>
                        <input type="text" placeholder="..." :id="key" v-model="newDataSample[key]" required>
                    </div>
                </div>

                <input type="submit" value="Tilføj">
            </fieldset>
        </form>
    </Content>


    <!-- Radio buttons -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Radio knapper og checkbokse</template>

        <span class="paragraph">
            Radio knapper og checkbokse indsættes som almindelige HTML <code>&lt;input&gt;</code>-elementer, efterfulgt af et <code>&lt;label&gt;</code>-element.
        </span>

        <div class="flexbox grow">
            <form @submit.prevent="">
                <input type="radio" id="One" name="radio" value="One">
                <label for="One">One</label><br>
                <input type="radio" id="Two" name="radio" value="Two">
                <label for="Two">Two</label><br>
                <input type="radio" id="Three" name="radio" value="Three">
                <label for="Three">Three</label><br>
            </form>

            <form @submit.prevent="">
                <input type="checkbox" id="One-C" name="One" value="One">
                <label for="One-C">One</label><br>
                <input type="checkbox" id="Two-C" name="Two" value="Two">
                <label for="Two-C">Two</label><br>
                <input type="checkbox" id="Three-C" name="Three" value="Three">
                <label for="Three-C">Three</label><br>
            </form>
        </div>
    </Content>

    
    <!-- Range slider -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Range slider</template>

        <span class="paragraph">
            Range sliders kan ligeledes gøres dynamiske. Brug Vue's <code>v-model</code>-tag til at knytte slideren til en variabel.
        </span>
        
        <h4 class="center"><span class="heavy">{{rangeValue}}</span> %</h4>
        <input v-model="rangeValue" type="range" min="0" max="100" value="50" :style="{ 'background': 'linear-gradient(to right,  var(--randers-color-light) 0%, var(--randers-color-light) '+rangeValue+'%, var(--color-border-dark) '+rangeValue+'%, var(--color-border-dark) 100%)' }">

        <span class="paragraph">
            Range sliders kan også bruges som f.eks. progress-bars, ved at sætte elementet som <code>disabled</code>.
        </span>

        <input type="range" min="0" max="100" :value="rangeValue" :style="{ 'background': 'linear-gradient(to right,  var(--randers-color-light) 0%, var(--randers-color-light) '+rangeValue+'%, var(--color-border-dark) '+rangeValue+'%, var(--color-border-dark) 100%)' }" disabled>

    </Content>


    <!-- Buttons  -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Knapper</template>

        <span class="paragraph">
            Knapper indsættes med <code>&lt;button&gt;</code>-tags, eller alternativt som et <code>&lt;input&gt;</code>-tag med type <code>submit</code> i en <code>form</code>. Knapper kan farves med predefinerede farveklasser.
        </span>
        
        <button >Almindelig knap</button>
        <button class="blue">Blå knap</button>
        <button class="green">Grøn knap</button>
        <button class="red">Rød knap</button>
        <button class="orange">Orange knap</button>

    </Content>


    <!-- Tags -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Tags</template>

        <span class="paragraph">
            Info tags indsættes som <code>&lt;span&gt;</code>-elementer med klassen <code>tag</code>. Tags kan farves med predefinerede farveklasser.
        </span>
        
        <span class="tag">Almindeligt tag</span>
        <span class="tag blue">Blåt tag</span>
        <span class="tag green">Grønt tag</span>
        <span class="tag red">Rødt tag</span>
        <span class="tag orange">Orange tag</span>
        <span class="tag randers">Randers tag</span>

    </Content>


    <!-- Alerts -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Beskeder</template>

        <span class="paragraph">
            Beskeder indsættes som <code>&lt;div&gt;</code>-elementer, og kan indeholde en <code>header</code>. Beskeder kan farves med predefinerede farveklasser.
        </span>

        <div class="paragraph">

            <div class="message" id="msg1">
                <div class="header">
                    Overskrift
                    <span class="float-right close" @click="deleteMessage('msg1')">x</span>
                </div>
                Her er en vigtig besked med en beskrivelse.
            </div>

        </div>

        <div class="flexbox">

            <div class="message blue" id="msg2">
                <div class="header">
                    Overskrift
                    <span class="float-right close" @click="deleteMessage('msg2')">x</span>
                </div>
                Her er en vigtig besked med en beskrivelse.
            </div>

            <div class="message green" id="msg3">
                <div class="header">
                    Overskrift
                    <span class="float-right close" @click="deleteMessage('msg3')">x</span>
                </div>
                Her er en vigtig besked med en beskrivelse.
            </div>

            <div class="message red" id="msg4">
                <div class="header">
                    Overskrift
                    <span class="float-right close" @click="deleteMessage('msg4')">x</span>
                </div>
                Her er en vigtig besked med en beskrivelse.
            </div>

            <div class="message orange" id="msg5">
                <div class="header">
                    Overskrift
                    <span class="float-right close" @click="deleteMessage('msg5')">x</span>
                </div>
                Her er en vigtig besked med en beskrivelse.
            </div>

            <div class="message randers" id="msg6">
                <div class="header">
                    Overskrift
                    <span class="float-right close" @click="deleteMessage('msg6')">x</span>
                </div>
                Her er en vigtig besked med en beskrivelse.
            </div>

        </div>
        
    </Content>

    
    <!-- Pagination -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Sidenummerering</template>

        <span class="paragraph">
            Sidenummering indsættes som <code>&lt;router-link&gt;</code>-elementer, i en <code>&lt;div&gt;</code> med klassen <code>pagination</code>.
            Nummeringerne kan have klasserne <code>disabled</code> eller <code>selected</code>.
        </span>
        
        <div class="paragraph">
            <div class="pagination">
                <router-link to="" class="disabled">&lt;</router-link>
                <router-link to="" class="selected">1</router-link>
                <router-link to="">2</router-link>
                <router-link to="">3</router-link>
                <router-link to="">4</router-link>
                <router-link to="">5</router-link>
                <router-link to="">&gt;</router-link>
            </div>
        </div>
        
    </Content>


    <!-- Milligram -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Header underretninger</template>

        <span class="paragraph">
            Tryk på knappen for at sætte en header underretning for menupunktet 'UI Templates'.
        </span>

        <form @submit.prevent="setHeaderAlert(newHeaderAlert)">
            <fieldset>
                <div class="flexbox">
                    <div>
                        <label for="newHeaderAlertTextbox" class="capitalize">Underretning</label>
                        <input type="text" placeholder="Skriv en underretning, f.eks. et tal .." id="newHeaderAlertTextbox" v-model="newHeaderAlert">
                    </div>
                </div>

                <input type="submit" value="Tilføj">
            </fieldset>
        </form>
        
    </Content>


    <!-- Milligram -->
    <Content>
        <template #icon>

        </template>
        <template #heading>Milligram CSS</template>

        <span class="paragraph">
            Dette template er baseret på Milligram, et minimalistisk CSS-framwork.
            Yderligere dokumentation på mere almindelig HTML-formatering, herunder typografi, lister mv. findes på <a href="https://milligram.io/#typography" target="_blank">Milligram's hjemmeside</a>.
        </span>
        
    </Content>

</template>