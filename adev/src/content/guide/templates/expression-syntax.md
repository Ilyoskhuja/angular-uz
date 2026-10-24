# Ifoda sintaksisi

Angular ifodalari (expressions) JavaScript'ga asoslangan, lekin baʼzi muhim jihatlarda farq qiladi. Bu qoʻllanma Angular ifodalari va standart JavaScript oʻrtasidagi oʻxshashlik va farqlarni koʻrib chiqadi.

## Qiymat literallari {#value-literals}

Angular JavaScript'dagi [literal qiymatlar](https://developer.mozilla.org/en-US/docs/Glossary/Literal)ning bir qismini qoʻllab-quvvatlaydi.

### Qoʻllab-quvvatlanadigan qiymat literallari {#supported-value-literals}

| Literal turi           | Misol qiymatlar                  |
| ---------------------- | ------------------------------- |
| String (satr)          | `'Hello'`, `"World"`            |
| Boolean                | `true`, `false`                 |
| Number (son)           | `123`, `3.14`                   |
| Object (obyekt)        | `{name: 'Alice'}`               |
| Array (massiv)         | `['Onion', 'Cheese', 'Garlic']` |
| null                   | `null`                          |
| RegExp                 | `/\d+/`                         |
| Shablon satri          | `` `Hello ${name}` ``           |
| Teglangan shablon satri | `` tag`Hello ${name}` ``        |

### Qoʻllab-quvvatlanmaydigan qiymat literallari {#unsupported-value-literals}

| Literal turi | Misol qiymatlar |
| ------------ | -------------- |
| BigInt       | `1n`           |

## Global obyektlar {#globals}

Angular ifodalari quyidagi [global obyektlarni](https://developer.mozilla.org/en-US/docs/Glossary/Global_object) qoʻllab-quvvatlaydi:

- [undefined](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/undefined)
- [$any](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#any)

Boshqa JavaScript global obyektlari qoʻllab-quvvatlanmaydi. Keng tarqalgan JavaScript global obyektlariga `Number`, `Boolean`, `NaN`, `Infinity`, `parseInt` va boshqalar kiradi.

## Lokal oʻzgaruvchilar {#local-variables}

Angular maʼlum kontekstlarda ifodalarda foydalanish uchun maxsus lokal oʻzgaruvchilarni avtomatik ravishda taqdim etadi. Bu maxsus oʻzgaruvchilar doimo dollar belgisi (`$`) bilan boshlanadi.

Masalan, `@for` bloklari `$index` kabi sikl haqidagi maʼlumotlarga mos keluvchi bir nechta lokal oʻzgaruvchilarni yaratadi.

## Qaysi operatorlar qoʻllab-quvvatlanadi? {#what-operators-are-supported}

### Qoʻllab-quvvatlanadigan operatorlar {#supported-operators}

Angular standart JavaScript'dagi quyidagi operatorlarni qoʻllab-quvvatlaydi.

| Operator                      | Misol(lar)                                     |
| ----------------------------- | ---------------------------------------------- |
| Qoʻshish / Birlashtirish      | `1 + 2`                                        |
| Ayirish                       | `52 - 3`                                       |
| Koʻpaytirish                  | `41 * 6`                                       |
| Boʻlish                       | `20 / 4`                                       |
| Qoldiq (Modul)                | `17 % 5`                                       |
| Darajaga koʻtarish            | `10 ** 3`                                      |
| Qavslar                       | `9 * (8 + 4)`                                  |
| Shartli (Ternar)              | `a > b ? true : false`                         |
| Va (Mantiqiy)                 | `&&`                                           |
| Yoki (Mantiqiy)               | `\|\|`                                         |
| Inkor (Mantiqiy)              | `!`                                            |
| Nullish Coalescing            | `possiblyNullValue ?? 'default'`               |
| Solishtirish operatorlari     | `<`, `<=`, `>`, `>=`, `==`, `===`, `!==`, `!=` |
| Unar manfiy                   | `-x`                                           |
| Unar musbat                   | `+y`                                           |
| Xususiyatga murojaat          | `person['name']`                               |
| typeof                        | `typeof 42`                                    |
| void                          | `void 1`                                       |
| in                            | `'model' in car`                               |
| instanceof                    | `car instanceof Automobile`                    |
| Tayinlash                     | `a = b`                                        |
| Inkrement                     | `a++`, `++a`                                   |
| Dekrement                     | `a--`, `--a`                                   |
| Qoʻshib tayinlash             | `a += b`                                       |
| Ayirib tayinlash              | `a -= b`                                       |
| Koʻpaytirib tayinlash         | `a *= b`                                       |
| Boʻlib tayinlash              | `a /= b`                                       |
| Qoldiq bilan tayinlash        | `a %= b`                                       |
| Darajaga koʻtarib tayinlash   | `a **= b`                                      |
| Mantiqiy VA bilan tayinlash   | `a &&= b`                                      |
| Mantiqiy YOKI bilan tayinlash | `a \|\|= b`                                    |
| Nullish Coalescing bilan tayinlash | `a ??= b`                                 |
| Obyekt literallarida spread   | `{...obj, foo: 'bar'}`                         |
| Massiv literallarida spread   | `[...arr, 1, 2, 3]`                            |
| Funksiya chaqiruvlarida rest  | `fn(...args)`                                  |
| Strelka funksiyasi (arrow function) | `items.filter((i) => i.active)`          |

NOTE: Tayinlash va inkrement/dekrement operatorlari faqat [hodisa tinglovchisi operatorlarida](#event-listener-statements) yaroqli. Ularni bogʻlash yoki interpolyatsiyada ishlatish kompilyatsiya xatosidir, agar ular strelka funksiyasi ichida boʻlmasa.

Strelka funksiyalari ifoda tanasiga ega boʻlishi shart. Strelka funksiyasi ichida pipe'lardan foydalanish mumkin emas, lekin strelka funksiyasini pipe'ga argument sifatida uzatishingiz mumkin.

Angular ifodalari bundan tashqari quyidagi nostandart operatorlarni ham qoʻllab-quvvatlaydi:

| Operator                        | Misol(lar)                     |
| ------------------------------- | ------------------------------ |
| [Pipe](/guide/templates/pipes)  | `{{ total \| currency }}`      |
| Ixtiyoriy zanjir (optional chaining)\* | `someObj.someProp?.nestedProp` |
| Null boʻlmaslik tasdigʻi (TypeScript) | `someObj!.someProp`       |

### Xavfsiz navigatsiya migratsiyasi {#safe-navigation-migration}

Angular 22'dan oldin ixtiyoriy zanjir operatori (`?.`) chap tomon `null` yoki `undefined` boʻlganda `null` qaytarar edi, standart JavaScript'dagi `?.` esa `undefined` qaytaradi.
Angular 22'dan boshlab Angular ifodalaridagi ixtiyoriy zanjir operatorining xatti-harakati standart JavaScript xatti-harakatiga moslashtirildi.

v22'ga migratsiya davomida `ng update` sxematikalari oldingi xatti-harakatni saqlab qolish uchun mavjud ifodalarga `$safeNavigationMigration` funksiyasini qoʻshadi.

```html
{{ $safeNavigationMigration(foo?.bar) }}
```

`$safeNavigationMigration` — bu **faqat vaqtinchalik migratsiya yordamchisi**. U kompilyatorga oʻralgan xavfsiz navigatsiya ifodasini standart JavaScript `?.` semantikasi oʻrniga eski, `null` qaytaruvchi semantika bilan kompilyatsiya qilishni buyuradi. Bu haqiqiy funksiya emas va uni TypeScript'dan chaqirish mumkin emas.

NOTE: `$safeNavigationMigration`'ni olib tashlash mumkin boʻlishi uchun ifodalarni `null` va `undefined` farqiga tayanmaydigan holga migratsiya qilishni afzal koʻring. Bu funksiya Angular'ning kelajakdagi versiyasida olib tashlanishi mumkin.

### Qoʻllab-quvvatlanmaydigan operatorlar {#unsupported-operators}

| Operator              | Misol(lar)                        |
| --------------------- | --------------------------------- |
| Barcha bitli operatorlar | `&`, `&=`, `~`, `\|=`, `^=` va h.k. |
| Obyekt destrukturizatsiyasi | `const { name } = person`    |
| Massiv destrukturizatsiyasi | `const [firstItem] = items`  |
| Vergul operatori      | `x = (x++, x)`                    |
| new                   | `new Car()`                       |

## Ifodalar uchun leksik kontekst {#lexical-context-for-expressions}

Angular ifodalari komponent klassi kontekstida, shuningdek tegishli [shablon oʻzgaruvchilari](/guide/templates/variables), lokal va global obyektlar kontekstida hisoblanadi.

Komponent klassi aʼzolariga murojaat qilganda `this` doimo nazarda tutiladi. Biroq, agar shablon aʼzo bilan bir xil nomli [shablon oʻzgaruvchisini](guide/templates/variables) eʼlon qilsa, oʻzgaruvchi oʻsha aʼzoni yashiradi (shadowing). Bunday klass aʼzosiga `this.`'ni aniq yozish orqali bir maʼnoli murojaat qilishingiz mumkin. Bu klass aʼzosini yashiradigan `@let` eʼlonini yaratishda, masalan, signalni toraytirish maqsadida, foydali boʻlishi mumkin.

## Eʼlonlar {#declarations}

Umuman olganda, Angular ifodalarida eʼlonlar qoʻllab-quvvatlanmaydi. Bunga quyidagilar kiradi, lekin ular bilan cheklanmaydi:

| Eʼlonlar                          | Misol(lar)                                  |
| --------------------------------- | ------------------------------------------- |
| Oʻzgaruvchilar                    | `let label = 'abc'`, `const item = 'apple'` |
| Funksiyalar                       | `function myCustomFunction() { }`           |
| Blok tanali strelka funksiyalari  | `() => { }`                                 |
| Klasslar                          | `class Rectangle { }`                       |

## Hodisa tinglovchisi operatorlari {#event-listener-statements}

Hodisa ishlov beruvchilari ifodalar emas, balki **operatorlar (statements)**dir. Ular Angular ifodalari bilan bir xil sintaksisning barchasini qoʻllab-quvvatlasa-da, ikkita asosiy farq mavjud:

1. Operatorlar tayinlash operatorlarini **qoʻllab-quvvatlaydi** (lekin destrukturizatsiya orqali tayinlashni emas)
1. Operatorlar pipe'larni **qoʻllab-quvvatlamaydi**
