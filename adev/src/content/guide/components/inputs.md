# Input xususiyatlari orqali maʼlumot qabul qilish

TIP: Bu qoʻllanma siz [Asoslar qoʻllanmasini](essentials) allaqachon oʻqib chiqqan deb hisoblaydi. Agar Angular'da yangi boʻlsangiz, avval oʻshani oʻqing. Agar boshqa veb freymvorklar bilan tanish boʻlsangiz, input xususiyatlari _props_'ga oʻxshaydi.

Komponentdan foydalanganingizda, odatda unga qandaydir maʼlumot uzatmoqchi boʻlasiz. Komponent qabul qiladigan maʼlumotlarni
**input**'larni eʼlon qilish orqali belgilaydi:

```ts {highlight:[6]}
import {Component, input} from '@angular/core';

@Component(/* ... */)
export class CustomSlider {
  // Declare an input named 'value' with a default value of zero.
  value = input(0);
}
```

Bu shablonda xususiyatga bogʻlash imkonini beradi:

```angular-html
<custom-slider [value]="50" />
```

Agar input sukut boʻyicha qiymatga ega boʻlsa, TypeScript turni sukut boʻyicha qiymatdan keltirib chiqaradi:

```ts
@Component(/* ... */)
export class CustomSlider {
  // TypeScript infers that this input is a number, returning InputSignal<number>.
  value = input(0);
}
```

Funksiyaga generik parametr koʻrsatib, input uchun turni aniq eʼlon qilishingiz mumkin.

Agar sukut boʻyicha qiymati boʻlmagan input oʻrnatilmasa, uning qiymati `undefined` boʻladi:

```ts
@Component(/* ... */)
export class CustomSlider {
  // Produces an InputSignal<number | undefined> because `value` may not be set.
  value = input<number>();
}
```

**Angular input'larni kompilyatsiya vaqtida statik tarzda qayd qiladi**. Input'larni ish vaqtida qoʻshish yoki olib tashlash mumkin emas.

`input` funksiyasi Angular kompilyatori uchun alohida maʼnoga ega. **`input` ni faqat komponent va direktiva xususiyatlarining initsializatorlarida chaqirishingiz mumkin.**

Komponent klassini kengaytirganda **input'lar bola klass tomonidan meros qilib olinadi.**

**Input nomlari katta-kichik harflarga sezgir.**

## Input'larni oʻqish {#reading-inputs}

`input` funksiyasi `InputSignal` qaytaradi. Qiymatni signalni chaqirish orqali oʻqishingiz mumkin:

```ts {highlight:[9]}
import {Component, input, computed} from '@angular/core';

@Component(/* ... */)
export class CustomSlider {
  // Declare an input named 'value' with a default value of zero.
  value = input(0);

  // Create a computed expression that reads the value input
  label = computed(() => `The slider's value is ${this.value()}`);
}
```

`input` funksiyasi tomonidan yaratilgan signallar faqat oʻqish uchun.

## Majburiy input'lar {#required-inputs}

`input` oʻrniga `input.required` ni chaqirib, input `required` (majburiy) ekanini eʼlon qilishingiz mumkin:

```ts {highlight:[4]}
@Component(/* ... */)
export class CustomSlider {
  // Declare a required input named value. Returns an `InputSignal<number>`.
  value = input.required<number>();
}
```

Angular komponent shablonda ishlatilganda majburiy input'larning _albatta_ oʻrnatilishini talab qiladi. Agar komponentni uning barcha majburiy input'larini koʻrsatmasdan ishlatmoqchi boʻlsangiz, Angular build vaqtida xato haqida xabar beradi.

Majburiy input'lar qaytariladigan `InputSignal` ning generik parametriga avtomatik ravishda `undefined` ni qoʻshmaydi.

## Input'larni sozlash {#configuring-inputs}

`input` funksiyasi ikkinchi parametr sifatida input ishlash tarzini oʻzgartirish imkonini beradigan konfiguratsiya obyektini qabul qiladi.

### Input transformatsiyalari {#input-transforms}

Input qiymati Angular tomonidan oʻrnatilganda uni oʻzgartirish uchun `transform` funksiyasini koʻrsatishingiz mumkin.

```ts {highlight:[6]}
@Component({
  selector: 'custom-slider',
  /*...*/
})
export class CustomSlider {
  label = input('', {transform: trimString});
}

function trimString(value: string | undefined): string {
  return value?.trim() ?? '';
}
```

```angular-html
<custom-slider [label]="systemVolume" />
```

Yuqoridagi misolda `systemVolume` qiymati oʻzgargan har safar Angular `trimString` ni ishga tushiradi va `label` ga natijani oʻrnatadi.

Input transformatsiyalarining eng keng tarqalgan qoʻllanilish holati — shablonlarda qiymat turlarining kengroq doirasini, koʻpincha `null` va `undefined` ni ham qabul qilish.

**Input transformatsiya funksiyasi build vaqtida statik tahlil qilinadigan boʻlishi shart.** Transformatsiya funksiyalarini shartli ravishda yoki ifodani hisoblash natijasi sifatida oʻrnatib boʻlmaydi.

**Input transformatsiya funksiyalari har doim [sof funksiyalar](https://en.wikipedia.org/wiki/Pure_function) boʻlishi kerak.** Transformatsiya funksiyasidan tashqaridagi holatga tayanish kutilmagan xatti-harakatga olib kelishi mumkin.

#### Turlarni tekshirish {#type-checking}

Input transformatsiyasini koʻrsatganingizda, transformatsiya funksiyasi parametrining turi shablonda input'ga oʻrnatilishi mumkin boʻlgan qiymatlar turlarini belgilaydi.

```ts
@Component(/* ... */)
export class CustomSlider {
  widthPx = input('', {transform: appendPx});
}

function appendPx(value: number): string {
  return `${value}px`;
}
```

Yuqoridagi misolda `widthPx` input'i `number` qabul qiladi, `InputSignal` xususiyati esa `string` qaytaradi.

#### Oʻrnatilgan transformatsiyalar {#built-in-transformations}

Angular eng keng tarqalgan ikki holat uchun ikkita oʻrnatilgan transformatsiya funksiyasini oʻz ichiga oladi: qiymatlarni boolean va raqamlarga keltirish.

```ts
import {Component, input, booleanAttribute, numberAttribute} from '@angular/core';

@Component(/* ... */)
export class CustomSlider {
  disabled = input(false, {transform: booleanAttribute});
  value = input(0, {transform: numberAttribute});
}
```

`booleanAttribute` standart HTML [boolean atributlarining](https://developer.mozilla.org/docs/Glossary/Boolean/HTML) xatti-harakatiga taqlid qiladi, bunda
atributning _mavjudligi_ "true" qiymatini bildiradi. Biroq, Angular'ning `booleanAttribute`'i `"false"` satrini aynan boolean `false` sifatida qabul qiladi.

`numberAttribute` berilgan qiymatni raqamga aylantirishga (parse) urinadi va aylantirish muvaffaqiyatsiz boʻlsa, `NaN` hosil qiladi.

### Input taxalluslari {#input-aliases}

Shablonlarda input nomini oʻzgartirish uchun `alias` opsiyasini koʻrsatishingiz mumkin.

```ts {highlight:[3]}
@Component(/* ... */)
export class CustomSlider {
  value = input(0, {alias: 'sliderValue'});
}
```

```angular-html
<custom-slider [sliderValue]="50" />
```

Bu taxallus (alias) xususiyatning TypeScript kodida ishlatilishiga taʼsir qilmaydi.

Umuman olganda komponentlar uchun input'larga taxallus berishdan saqlanish kerak boʻlsa-da, bu imkoniyat asl nom uchun taxallusni saqlab qolgan holda xususiyatlarni qayta nomlash yoki tabiiy DOM elementi xususiyatlari nomlari bilan toʻqnashuvlardan qochish uchun foydali boʻlishi mumkin.

## Model input'lar {#model-inputs}

**Model input'lar** — komponentga yangi qiymatlarni oʻz ota komponentiga qaytarib uzatish imkonini beradigan alohida turdagi input.

Komponent yaratganingizda model input'ni standart input yaratganingizga oʻxshash tarzda aniqlashingiz mumkin.

Ikkala turdagi input ham kimgadir xususiyatga qiymat bogʻlash imkonini beradi. Biroq, **model input'lar komponent muallifiga xususiyatga qiymat yozish imkonini beradi**. Agar xususiyat ikki tomonlama bogʻlash orqali bogʻlangan boʻlsa, yangi qiymat oʻsha bogʻlashga tarqaladi.

```ts
@Component(/* ... */)
export class CustomSlider {
  // Define a model input named "value".
  value = model(0);

  increment() {
    // Update the model input with a new value, propagating the value to any bindings.
    this.value.update((oldValue) => oldValue + 10);
  }
}

@Component({
  /* ... */
  // Using the two-way binding syntax means that any changes to the slider's
  // value automatically propagate back to the `volume` signal.
  // Note that this binding uses the signal *instance*, not the signal value.
  template: `<custom-slider [(value)]="volume" />`,
})
export class MediaControls {
  // Create a writable signal for the `volume` local state.
  volume = signal(0);
}
```

Yuqoridagi misolda `CustomSlider` oʻzining `value` model input'iga qiymatlar yozishi mumkin, bu esa oʻsha qiymatlarni `MediaControls` dagi `volume` signaliga qaytarib tarqatadi. Bu bogʻlash `value` va `volume` qiymatlarini sinxron holda saqlaydi. Eʼtibor bering, bogʻlash signalning _qiymatini_ emas, `volume` signalining nusxasini (instance) uzatadi.

Boshqa jihatlarda model input'lar standart input'larga oʻxshash ishlaydi. Qiymatni signal funksiyasini chaqirish orqali, jumladan `computed` va `effect` kabi [reaktiv kontekstlarda](guide/signals#reactive-contexts) ham oʻqishingiz mumkin.

Shablonlarda ikki tomonlama bogʻlash haqida batafsil maʼlumot uchun [Ikki tomonlama bogʻlash](guide/templates/two-way-binding) boʻlimiga qarang.

### Oddiy xususiyatlar bilan ikki tomonlama bogʻlash {#two-way-binding-with-plain-properties}

Oddiy JavaScript xususiyatini model input'ga bogʻlashingiz mumkin.

```angular-ts
@Component({
  /* ... */
  // `value` is a model input.
  // The parenthesis-inside-square-brackets syntax (aka "banana-in-a-box") creates a two-way binding
  template: '<custom-slider [(value)]="volume" />',
})
export class MediaControls {
  protected volume = 0;
}
```

Yuqoridagi misolda `CustomSlider` oʻzining `value` model input'iga qiymatlar yozishi mumkin, bu esa oʻsha qiymatlarni `MediaControls` dagi `volume` xususiyatiga qaytarib tarqatadi. Bu bogʻlash `value` va `volume` qiymatlarini sinxron holda saqlaydi.

### Yashirin `change` hodisalari {#implicit-change-events}

Komponent yoki direktivada model input eʼlon qilganingizda, Angular oʻsha model uchun avtomatik ravishda tegishli [output](guide/components/outputs) yaratadi. Output'ning nomi — model input nomiga "Change" qoʻshimchasi qoʻshilgan koʻrinishda boʻladi.

```ts
@Directive(/* ... */)
export class CustomCheckbox {
  // This automatically creates an output named "checkedChange".
  // Can be subscribed to using `(checkedChange)="handler()"` in the template.
  checked = model(false);
}
```

Angular model input'ga uning `set` yoki `update` metodlarini chaqirib yangi qiymat yozgan har safar bu change hodisasini chiqaradi.

Output'lar haqida batafsil maʼlumot uchun [Output'lar bilan maxsus hodisalar](guide/components/outputs) boʻlimiga qarang.

### Model input'larni sozlash {#customizing-model-inputs}

Model input'ni standart input bilan bir xil tarzda [majburiy](#required-inputs) deb belgilashingiz yoki unga [taxallus](#input-aliases) berishingiz mumkin.

Model input'lar input transformatsiyalarini qoʻllab-quvvatlamaydi.

### Model input'larni qachon ishlatish kerak {#when-to-use-model-inputs}

Komponent ikki tomonlama bogʻlashni qoʻllab-quvvatlashini istasangiz, model input'lardan foydalaning. Bu odatda komponent foydalanuvchi harakatiga asoslanib qiymatni oʻzgartirish uchun mavjud boʻlganda oʻrinli. Koʻpincha sana tanlagich (date picker) yoki combobox kabi maxsus forma elementlari oʻz asosiy qiymati uchun model input'lardan foydalanishi kerak.

## Input nomlarini tanlash {#choosing-input-names}

HTMLElement kabi DOM elementlaridagi xususiyatlar bilan toʻqnashadigan input nomlarini tanlashdan saqlaning. Nomlar toʻqnashuvi bogʻlangan xususiyat komponentga yoki DOM elementiga tegishli ekani haqida chalkashlik keltirib chiqaradi.

Komponent selektorlarida qilganingizdek, komponent input'lariga prefiks qoʻshishdan saqlaning. Berilgan element faqat bitta komponentga host boʻlishi mumkinligi sababli, har qanday maxsus xususiyatlar komponentga tegishli deb hisoblanishi mumkin.

## Input'larni `@Input` dekoratori bilan eʼlon qilish {#declaring-inputs-with-the-input-decorator}

TIP: Angular jamoasi yangi loyihalar uchun signalga asoslangan `input` funksiyasidan foydalanishni tavsiya qilsa-da, dekoratorga asoslangan asl `@Input` API'si toʻliq qoʻllab-quvvatlanishda davom etadi.

Shuningdek, komponent input'larini xususiyatga `@Input` dekoratorini qoʻshish orqali ham eʼlon qilishingiz mumkin:

```ts {highlight:[3]}
@Component(/* ... */)
export class CustomSlider {
  @Input() value = 0;
}
```

Input'ga bogʻlash signalga asoslangan va dekoratorga asoslangan input'larda bir xil:

```angular-html
<custom-slider [value]="50" />
```

### Dekoratorga asoslangan input'larni sozlash {#customizing-decorator-based-inputs}

`@Input` dekoratori input ishlash tarzini oʻzgartirish imkonini beradigan konfiguratsiya obyektini qabul qiladi.

#### Majburiy input'lar {#required-inputs-decorator}

Berilgan input har doim qiymatga ega boʻlishini talab qilish uchun `required` opsiyasini koʻrsatishingiz mumkin.

```ts {highlight:[3]}
@Component(/* ... */)
export class CustomSlider {
  @Input({required: true}) value = 0;
}
```

Agar komponentni uning barcha majburiy input'larini koʻrsatmasdan ishlatmoqchi boʻlsangiz, Angular build vaqtida xato haqida xabar beradi.

#### Input transformatsiyalari {#input-transforms-decorator}

Input qiymati Angular tomonidan oʻrnatilganda uni oʻzgartirish uchun `transform` funksiyasini koʻrsatishingiz mumkin. Bu transformatsiya funksiyasi yuqorida tavsiflangan signalga asoslangan input'lar uchun transformatsiya funksiyalari bilan bir xil ishlaydi.

```ts {highlight:[6]}
@Component({
  selector: 'custom-slider',
  ...
})
export class CustomSlider {
  @Input({transform: trimString}) label = '';
}

function trimString(value: string | undefined) {
  return value?.trim() ?? '';
}
```

#### Input taxalluslari {#input-aliases-decorator}

Shablonlarda input nomini oʻzgartirish uchun `alias` opsiyasini koʻrsatishingiz mumkin.

```ts {highlight:[3]}
@Component(/* ... */)
export class CustomSlider {
  @Input({alias: 'sliderValue'}) value = 0;
}
```

```angular-html
<custom-slider [sliderValue]="50" />
```

`@Input` dekoratori konfiguratsiya obyekti oʻrniga taxallusni birinchi parametr sifatida ham qabul qiladi.

Input taxalluslari yuqorida tavsiflangan signalga asoslangan input'lar bilan bir xil tarzda ishlaydi.

### Getter va setter'li input'lar {#inputs-with-getters-and-setters}

Dekoratorga asoslangan input'lardan foydalanganda, getter va setter bilan amalga oshirilgan xususiyat input boʻlishi mumkin:

```ts
export class CustomSlider {
  @Input()
  get value(): number {
    return this.internalValue;
  }

  set value(newValue: number) {
    this.internalValue = newValue;
  }

  private internalValue = 0;
}
```

Hatto faqat ochiq (public) setter aniqlash orqali _faqat yozish uchun_ input yaratishingiz ham mumkin:

```ts
export class CustomSlider {
  @Input()
  set value(newValue: number) {
    this.internalValue = newValue;
  }

  private internalValue = 0;
}
```

Imkon boʻlsa, **getter va setter'lar oʻrniga input transformatsiyalaridan foydalanishni afzal koʻring**.

Murakkab yoki qimmat getter va setter'lardan saqlaning. Angular input'ning setter'ini bir necha marta chaqirishi mumkin, bu esa setter DOM bilan ishlash kabi qimmat amallarni bajarsa, ilova unumdorligiga salbiy taʼsir qilishi mumkin.

## Input'larni `@Component` dekoratorida koʻrsatish {#specify-inputs-in-the-component-decorator}

`@Input` dekoratoriga qoʻshimcha ravishda, komponent input'larini `@Component` dekoratoridagi `inputs` xususiyati orqali ham koʻrsatishingiz mumkin. Bu komponent xususiyatni asosiy (base) klassdan meros qilib olganda foydali boʻlishi mumkin:

```ts {highlight:[4]}
// `CustomSlider` inherits the `disabled` property from `BaseSlider`.
@Component({
  ...,
  inputs: ['disabled'],
})
export class CustomSlider extends BaseSlider { }
```

Bundan tashqari, `inputs` roʻyxatida satr ichida ikki nuqtadan keyin taxallusni yozib, input taxallusini ham koʻrsatishingiz mumkin:

```ts {highlight:[4]}
// `CustomSlider` inherits the `disabled` property from `BaseSlider`.
@Component({
  ...,
  inputs: ['disabled: sliderDisabled'],
})
export class CustomSlider extends BaseSlider { }
```
