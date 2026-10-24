# Boshqaruv oqimi

Angular shablonlari elementlarni shartli koʻrsatish, yashirish va takrorlash imkonini beruvchi boshqaruv oqimi (control flow) bloklarini qoʻllab-quvvatlaydi.

## `@if`, `@else if` va `@else` bilan kontentni shartli koʻrsatish {#conditionally-display-content-with-if-else-if-and-else}

`@if` bloki shart ifodasi rost (truthy) boʻlganda oʻz kontentini shartli koʻrsatadi:

```angular-html
@if (a > b) {
  <p>{{ a }} is greater than {{ b }}</p>
}
```

Agar muqobil kontentni koʻrsatmoqchi boʻlsangiz, buni istalgan sondagi `@else if` bloklari va yagona `@else` blokini berish orqali qilishingiz mumkin.

```angular-html
@if (a > b) {
  {{ a }} is greater than {{ b }}
} @else if (b > a) {
  {{ a }} is less than {{ b }}
} @else {
  {{ a }} is equal to {{ b }}
}
```

### Shart ifodasining natijasiga murojaat qilish {#referencing-the-conditional-expressions-result}

`@if` sharti shart ifodasining natijasini blok ichida qayta foydalanish uchun oʻzgaruvchiga saqlashni qoʻllab-quvvatlaydi.

```angular-html
@if (user.profile.settings.startDate; as startDate) {
  {{ startDate }}
}
```

Bu shablon ichida oʻqish va qoʻllab-quvvatlash osonroq boʻladigan uzunroq ifodalarga murojaat qilish uchun foydali boʻlishi mumkin.

## `@for` bloki bilan kontentni takrorlash {#repeat-content-with-the-for-block}

`@for` bloki kolleksiya boʻylab aylanib, blok kontentini takroran render qiladi. Kolleksiya istalgan JavaScript [iterable](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Iteration_protocols) obyekti boʻlishi mumkin, lekin Angular `Array` qiymatlari uchun qoʻshimcha unumdorlik optimizatsiyalariga ega.

Odatiy `@for` sikli quyidagicha koʻrinadi:

```angular-html
@for (item of items; track item.id) {
  {{ item.name }}
}
```

Angular'ning `@for` bloki JavaScript'dagi `continue` yoki `break` kabi oqimni oʻzgartiruvchi operatorlarni qoʻllab-quvvatlamaydi.

### `@for` bloklarida `track` nima uchun muhim? {#why-is-track-in-for-blocks-important}

`track` ifodasi Angular'ga maʼlumotlaringiz va sahifadagi DOM tugunlari oʻrtasidagi bogʻliqlikni saqlab turish imkonini beradi. Bu Angular'ga maʼlumotlar oʻzgarganda minimal zarur DOM operatsiyalarini bajarish orqali unumdorlikni optimallashtirish imkonini beradi.

`track`'dan samarali foydalanish maʼlumotlar kolleksiyalari boʻylab aylanganda ilovangizning render qilish unumdorligini sezilarli darajada yaxshilashi mumkin.

`track` ifodasida har bir elementni yagona tarzda identifikatsiya qiluvchi xususiyatni tanlang. Agar maʼlumotlar modelingizda yagona identifikatsiya qiluvchi xususiyat, odatda `id` yoki `uuid`, boʻlsa, shu qiymatdan foydalaning. Agar maʼlumotlaringizda bunday maydon boʻlmasa, uni qoʻshishni jiddiy oʻylab koʻring.

Hech qachon oʻzgarmaydigan statik kolleksiyalar uchun Angular'ga har bir elementni kolleksiyadagi indeksi boʻyicha kuzatishni aytish uchun `$index`'dan foydalanishingiz mumkin.

Agar boshqa variant boʻlmasa, elementning oʻzini kuzatish kaliti sifatida ishlatishingiz mumkin. Bu Angular'ga elementni uchlik tenglik operatori (`===`) orqali referens identikligi boʻyicha kuzatishni aytadi. Imkon qadar bu variantdan qoching, chunki u render yangilanishlarini sezilarli darajada sekinlashtirishi mumkin: Angular qaysi maʼlumot elementi qaysi DOM tugunlariga mos kelishini aniqlay olmaydi.

```angular-html
@for (item of items; track item) {
  {{ item.name }}
}
```

NOTE: `*ngFor`'dan farqli oʻlaroq, `@for` bloki view'ni qayta ishlatishga ustuvorlik beradi. Agar kuzatilayotgan xususiyat oʻzgarsa, lekin obyekt referensi oʻsha-oʻsha qolsa, Angular butun elementni yoʻq qilib qayta yaratish oʻrniga view'ning bogʻlashlarini (komponent input'lari ham kiradi) yangilaydi.

### `@for` bloklaridagi kontekst oʻzgaruvchilari {#contextual-variables-in-for-blocks}

`@for` bloklari ichida bir nechta yashirin (implicit) oʻzgaruvchilar doimo mavjud:

| Oʻzgaruvchi | Maʼnosi                                        |
| -------- | --------------------------------------------- |
| `$count` | Aylanilayotgan kolleksiyadagi elementlar soni |
| `$index` | Joriy qatorning indeksi                      |
| `$first` | Joriy qator birinchi qator ekanligi      |
| `$last`  | Joriy qator oxirgi qator ekanligi       |
| `$even`  | Joriy qator indeksi juft ekanligi         |
| `$odd`   | Joriy qator indeksi toq ekanligi          |

Bu oʻzgaruvchilar doimo shu nomlar bilan mavjud, lekin ularga `let` segmenti orqali taxallus (alias) berish mumkin:

```angular-html
@for (item of items; track item.id; let idx = $index, e = $even) {
  <p>Item #{{ idx }}: {{ item.name }}</p>
}
```

Taxallus berish `@for` bloklarini bir-birining ichiga joylashtirganda foydali: bu ichki `@for` blokidan tashqi `@for` blokining oʻzgaruvchilarini oʻqish imkonini beradi.

### `@empty` bloki bilan `@for` bloklari uchun zaxira variant berish {#providing-a-fallback-for-for-blocks-with-the-empty-block}

Ixtiyoriy ravishda `@for` bloki kontentidan keyin darhol `@empty` boʻlimini qoʻshishingiz mumkin. `@empty` blokining kontenti elementlar boʻlmaganda koʻrsatiladi:

```angular-html
@for (item of items; track item.name) {
  <li>{{ item.name }}</li>
} @empty {
  <li>There are no items.</li>
}
```

## `@switch` bloki bilan kontentni shartli koʻrsatish {#conditionally-display-content-with-the-switch-block}

`@if` bloki koʻp holatlar uchun ajoyib boʻlsa-da, `@switch` bloki maʼlumotlarni shartli render qilish uchun muqobil sintaksisni taqdim etadi. Uning sintaksisi JavaScript'dagi `switch` operatoriga juda oʻxshaydi.

```angular-html
@switch (userPermissions) {
  @case ('admin') {
    <app-admin-dashboard />
  }
  @case ('reviewer')
  @case ('editor') {
    <app-editor-dashboard />
  }
  @default {
    <app-viewer-dashboard />
  }
}
```

Shart ifodasining qiymati case ifodasi bilan uchlik tenglik (`===`) operatori orqali solishtiriladi.

**`@switch`'da fallthrough yoʻq**, shuning uchun blokda `break` yoki `return` operatorining ekvivalenti kerak emas.

Ketma-ket `@case` operatorlarini yozish orqali bitta blok uchun bir nechta shart koʻrsatishingiz mumkin.

Ixtiyoriy ravishda `@default` blokini qoʻshishingiz mumkin. `@default` blokining kontenti oldingi case ifodalarining hech biri switch qiymatiga mos kelmaganda koʻrsatiladi.

Agar hech bir `@case` ifodaga mos kelmasa va `@default` bloki boʻlmasa, hech narsa koʻrsatilmaydi.

### Toʻliqlikni (exhaustive) tur tekshiruvi {#exhaustive-type-checking}

`@switch` toʻliqlik tur tekshiruvini (exhaustive type checking) qoʻllab-quvvatlaydi, bu Angular'ga kompilyatsiya vaqtida union turning barcha mumkin boʻlgan qiymatlari qayta ishlanganini tekshirish imkonini beradi.

`@default never;` yozish orqali siz boshqa qolgan holatlar boʻlmasligi kerakligini aniq eʼlon qilasiz. Agar union tur keyinchalik kengaytirilsa va yangi holat @case bilan qoplanmasa, Angular'ning shablon tur tekshiruvchisi xato haqida xabar beradi va bu yetishmayotgan shoxlarni erta aniqlashga yordam beradi.

NOTE: Toʻliqlik tekshiruvi TypeScript'ning tur toraytirishiga (type narrowing) tayanadi, bu esa faqat oʻzgaruvchilar bilan ishlaydi. Agar switch sharti funksiya chaqiruvi yoki signal boʻlsa (masalan, `@switch (state())`), bu ishlamaydi. Buni chetlab oʻtish uchun signalni `@let` oʻzgaruvchisiga tayinlang, masalan: `@let mySignal = this.mySignal()`.

```angular-ts
@Component({
  template: `
    @switch (state) {
      @case ('loggedOut') {
        <button>Login</button>
      }

      @case ('loggedIn') {
        <p>Welcome back!</p>
      }

      @default never;
      <!-- throws because @case ('loading') is missing -->
    }
  `,
})
export class AppComponent {
  state: 'loggedOut' | 'loading' | 'loggedIn' = 'loggedOut';
}
```

Switch qilinayotgan ifoda union ichida joylashgan boʻlsa, toʻliqlikni tekshirish uchun ifodani aniq koʻrsatishingiz shart.

<!-- prettier-ignore -->
```angular-ts
@Component({
  template: `
    @switch (state.mode) {
      @case ('show') {
        {{ state.menu }};
      }
      @case ('hide') {}
      @default never(state);
    }
  `,
})
export class App {
  state!: {mode: 'hide'} | {mode: 'show'; menu: number};
}
```
