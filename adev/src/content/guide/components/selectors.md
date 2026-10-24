# Komponent selektorlari

TIP: Bu qoʻllanma siz [Asoslar qoʻllanmasini](essentials) allaqachon oʻqib chiqqan deb hisoblaydi. Agar Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Har bir komponent uning qanday ishlatilishini belgilaydigan
[CSS selektorini](https://developer.mozilla.org/docs/Web/CSS/CSS_selectors)
aniqlaydi:

```angular-ts {highlight: [2]}
@Component({
  selector: 'profile-photo',
  ...
})
export class ProfilePhoto { }
```

Komponentdan _boshqa_ komponentlarning shablonlarida mos keluvchi HTML element yaratish orqali foydalanasiz:

```angular-ts {highlight: [3]}
@Component({
  template: `
    <profile-photo />
    <button>Upload a new profile photo</button>`,
  ...,
})
export class UserProfile { }
```

**Angular selektorlarni kompilyatsiya vaqtida statik tarzda moslashtiradi**. Ish vaqtida DOM'ni Angular bogʻlashlari yoki
DOM API'lari orqali oʻzgartirish render qilinadigan komponentlarga taʼsir qilmaydi.

**Bir element faqat bitta komponent selektoriga mos kelishi mumkin.** Agar bir nechta komponent selektori bitta
elementga mos kelsa, Angular xato haqida xabar beradi.

**Komponent selektorlari katta-kichik harflarga sezgir.**

## Selektor turlari {#types-of-selectors}

Angular komponent selektorlarida
[asosiy CSS selektor turlarining](https://developer.mozilla.org/docs/Web/CSS/CSS_Selectors)
cheklangan bir qismini qoʻllab-quvvatlaydi:

| **Selektor turi**  | **Tavsif**                                                                                                       | **Misollar**                  |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| Tur selektori      | Elementlarni HTML teg nomi yoki tugun (node) nomi boʻyicha moslashtiradi.                                        | `profile-photo`               |
| Atribut selektori  | Elementlarni HTML atributining mavjudligi va, ixtiyoriy ravishda, oʻsha atributning aniq qiymati boʻyicha moslashtiradi. | `[dropzone]` `[type="reset"]` |
| Klass selektori    | Elementlarni CSS klassining mavjudligi boʻyicha moslashtiradi.                                                   | `.menu-item`                  |

Atribut qiymatlari uchun Angular tenglik (`=`) operatori bilan aniq atribut qiymatini moslashtirishni
qoʻllab-quvvatlaydi. Angular boshqa atribut qiymati operatorlarini qoʻllab-quvvatlamaydi.

Angular komponent selektorlari kombinatorlarni, jumladan
[avlod kombinatorini](https://developer.mozilla.org/docs/Web/CSS/Descendant_combinator)
yoki [bola kombinatorini](https://developer.mozilla.org/docs/Web/CSS/Child_combinator) qoʻllab-quvvatlamaydi.

Angular komponent selektorlari
[nomlar fazosini (namespace)](https://developer.mozilla.org/docs/Web/SVG/Namespaces_Crash_Course) koʻrsatishni qoʻllab-quvvatlamaydi.

### `:not` psevdo-klassi {#the-not-pseudo-class}

Angular [`:not` psevdo-klassini](https://developer.mozilla.org/docs/Web/CSS/:not) qoʻllab-quvvatlaydi.
Komponent selektori qaysi elementlarga mos kelishini cheklash uchun bu psevdo-klassni istalgan boshqa
selektorga qoʻshishingiz mumkin. Masalan, `[dropzone]` atribut selektorini aniqlab, uning `textarea`
elementlariga mos kelishining oldini olishingiz mumkin:

```angular-ts {highlight: [2]}
@Component({
  selector: '[dropzone]:not(textarea)',
  ...
})
export class DropZone { }
```

Angular komponent selektorlarida boshqa hech qanday psevdo-klass yoki psevdo-elementni qoʻllab-quvvatlamaydi.

### Selektorlarni birlashtirish {#combining-selectors}

Bir nechta selektorni ketma-ket yozish orqali birlashtirishingiz mumkin. Masalan, `type="reset"` koʻrsatilgan
`<button>` elementlarini moslashtirishingiz mumkin:

```angular-ts {highlight: [2]}
@Component({
  selector: 'button[type="reset"]',
  ...
})
export class ResetButton { }
```

Shuningdek, vergul bilan ajratilgan roʻyxat orqali bir nechta selektorni aniqlashingiz mumkin:

```angular-ts {highlight: [2]}
@Component({
  selector: 'drop-zone, [dropzone]',
  ...
})
export class DropZone { }
```

Angular roʻyxatdagi selektorlarning _istalgan biriga_ mos keladigan har bir element uchun komponent yaratadi.

## Selektor tanlash {#choosing-a-selector}

Komponentlarning aksariyati selektor sifatida maxsus element nomidan (custom element name) foydalanishi kerak. Barcha maxsus
element nomlari [HTML spetsifikatsiyasida](https://html.spec.whatwg.org/multipage/custom-elements.html#valid-custom-element-name)
tavsiflanganidek, defis belgisini oʻz ichiga olishi kerak.
Sukut boʻyicha Angular mavjud komponentlarning hech biriga mos kelmaydigan maxsus teg nomiga duch kelsa, xato haqida
xabar beradi va shu orqali komponent nomlarini notoʻgʻri yozish tufayli kelib chiqadigan xatolarning oldini oladi.

Angular shablonlarida [tabiiy (native) maxsus elementlardan](https://developer.mozilla.org/docs/Web/Web_Components) foydalanish
haqida batafsil maʼlumot uchun [Komponentlarning kengaytirilgan konfiguratsiyasi](guide/components/advanced-configuration)
boʻlimiga qarang.

### Selektor prefikslari {#selector-prefixes}

Angular jamoasi loyihangiz ichida aniqlangan barcha maxsus komponentlar uchun qisqa va bir xil prefiksdan
foydalanishni tavsiya qiladi. Masalan, agar YouTube'ni Angular bilan yaratmoqchi boʻlsangiz, komponentlaringizga
`yt-` prefiksini qoʻyib, `yt-menu`, `yt-player` va shu kabi komponentlar yaratishingiz mumkin. Selektorlaringizni shu tarzda
nomlar fazosiga ajratish muayyan komponent qayerdan kelganini darhol tushunarli qiladi. Sukut
boʻyicha Angular CLI `app-` prefiksidan foydalanadi.

IMPORTANT: Angular oʻzining freymvork API'lari uchun `ng` selektor prefiksidan foydalanadi. Oʻzingizning maxsus komponentlaringiz uchun hech qachon `ng` ni selektor prefiksi sifatida ishlatmang.

### Atribut selektorini qachon ishlatish kerak {#when-to-use-an-attribute-selector}

Standart tabiiy element ustida komponent yaratmoqchi boʻlsangiz, atribut selektoridan foydalanishni
koʻrib chiqishingiz kerak. Masalan, maxsus tugma komponenti yaratmoqchi boʻlsangiz, atribut selektoridan foydalanib
standart `<button>` elementining afzalliklaridan foydalanishingiz mumkin:

```angular-ts {highlight: [2]}
@Component({
  selector: 'button[yt-upload]',
   ...
})
export class YouTubeUploadButton { }
```

Bu yondashuv komponentdan foydalanuvchilarga qoʻshimcha ish qilmasdan elementning barcha standart API'laridan
toʻgʻridan-toʻgʻri foydalanish imkonini beradi. Bu `aria-label` kabi ARIA atributlari uchun ayniqsa qimmatli.

Angular mavjud komponentga mos kelmaydigan maxsus atributlarga duch kelganda xato haqida xabar bermaydi.
Atribut selektorli komponentlardan foydalanilganda, ulardan foydalanuvchilar komponentni yoki uning NgModule'ini
import qilishni unutib qoʻyishi mumkin, natijada komponent render qilinmaydi.
Qoʻshimcha maʼlumot uchun [Komponentlarni import qilish va ishlatish](guide/components#imports-in-the-component-decorator) boʻlimiga qarang.

Atribut selektorlarini aniqlaydigan komponentlar kichik harfli, defis bilan ajratilgan (dash-case) atributlardan foydalanishi kerak.
Yuqorida tavsiflangan prefiks qoʻyish tavsiyasiga ham amal qilishingiz mumkin.
