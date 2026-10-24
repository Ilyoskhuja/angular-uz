# Yengil inyeksiya tokenlari yordamida klient ilovasi hajmini optimallashtirish

Bu sahifa kutubxona dasturchilariga tavsiya etiladigan bogʻliqliklarni inyeksiya qilish usulining konseptual umumiy koʻrinishini beradi.
Kutubxonangizni _yengil inyeksiya tokenlari_ (lightweight injection tokens) bilan loyihalash kutubxonangizdan foydalanadigan klient ilovalarining bundle hajmini optimallashtirishga yordam beradi.

Tree-shaking qilinadigan provider'lardan foydalanib, bundle hajmini optimallashtirish uchun komponentlaringiz va inyeksiya qilinadigan servislaringiz orasidagi bogʻliqlik tuzilmasini boshqarishingiz mumkin.
Bu odatda taqdim etilgan komponent yoki servis ilova tomonidan hech qachon haqiqatan ishlatilmasa, kompilyator uning kodini bundle'dan olib tashlay olishini taʼminlaydi.

Angular inyeksiya tokenlarini saqlash usuli tufayli bunday ishlatilmagan komponent yoki servis baribir bundle'ga tushib qolishi mumkin.
Bu sahifa yengil inyeksiya tokenlaridan foydalanib, toʻgʻri tree-shaking'ni qoʻllab-quvvatlovchi bogʻliqliklarni inyeksiya qilish dizayn namunasini tavsiflaydi.

Yengil inyeksiya tokeni dizayn namunasi kutubxona dasturchilari uchun ayniqsa muhim.
U ilova kutubxonangiz imkoniyatlarining faqat bir qismidan foydalanganda, ishlatilmagan kodni klient ilovasining bundle'idan olib tashlash mumkinligini taʼminlaydi.

Ilova kutubxonangizdan foydalanganda, kutubxonangiz taqdim etadigan, lekin klient ilovasi ishlatmaydigan baʼzi servislar boʻlishi mumkin.
Bunday holda ilova dasturchisi oʻsha servis tree-shaking qilinishini va kompilyatsiya qilingan ilova hajmiga taʼsir qilmasligini kutadi.
Ilova dasturchisi kutubxonadagi tree-shaking muammosi haqida bila olmagani yoki uni tuzata olmagani sababli, buni qilish kutubxona dasturchisining masʼuliyatidir.
Ishlatilmagan komponentlarning saqlanib qolishini oldini olish uchun kutubxonangiz yengil inyeksiya tokeni dizayn namunasidan foydalanishi kerak.

## Tokenlar qachon saqlanib qoladi {#when-tokens-are-retained}

Token saqlanib qolish holati qanday sharoitda yuz berishini yaxshiroq tushuntirish uchun kutubxona kartasi (library-card) komponentini taqdim etuvchi kutubxonani koʻrib chiqaylik.
Bu komponent tanadan (body) iborat va ixtiyoriy sarlavha (header) qismini oʻz ichiga olishi mumkin:

```html
<lib-card>
  <lib-header>…</lib-header>
</lib-card>
```

Ehtimoliy realizatsiyada `<lib-card>` komponenti `<lib-header>` va `<lib-body>` elementlarini olish uchun quyidagi kabi `contentChild` yoki `contentChildren` funksiyasidan foydalanadi:

```ts {highlight: [14]}
import {Component, contentChild} from '@angular/core';

@Component({
  selector: 'lib-header',
  …,
})
class LibHeader {}

@Component({
  selector: 'lib-card',
  …,
})
class LibCard {
  readonly header = contentChild(LibHeader);
}
```

`<lib-header>` ixtiyoriy boʻlgani uchun element shablonda oʻzining minimal shaklida, `<lib-card />` koʻrinishida, paydo boʻlishi mumkin.
Bu holda `<lib-header>` ishlatilmaydi va siz uning tree-shaking qilinishini kutgan boʻlardingiz, lekin aslida bunday boʻlmaydi.
Buning sababi shundaki, `LibCard` aslida `LibHeader`'ga ikkita havolani oʻz ichiga oladi:

```ts
readonly header = contentChild(LibHeader);
```

- Bu havolalardan biri _tur pozitsiyasida_ (type position) -- yaʼni u `LibHeader`'ni tur sifatida koʻrsatadi: `readonly header: Signal<LibHeader|undefined>`.
- Ikkinchi havola _qiymat pozitsiyasida_ (value position) -- yaʼni `LibHeader` `contentChild` funksiyasiga uzatiladigan qiymat: `contentChild(LibHeader)`.

Kompilyator bu pozitsiyalardagi token havolalariga turlicha ishlov beradi:

- Kompilyator _tur pozitsiyasidagi_ havolalarni TypeScript'dan konvertatsiya qilgandan keyin oʻchirib tashlaydi, shuning uchun ular tree-shaking'ga taʼsir qilmaydi.
- Kompilyator _qiymat pozitsiyasidagi_ havolalarni ishga tushirish vaqtida saqlab qolishi kerak, bu esa komponentning tree-shaking qilinishiga **toʻsqinlik qiladi**.

Misolda kompilyator qiymat pozitsiyasida uchraydigan `LibHeader` tokenini saqlab qoladi.
Bu, ilova `<lib-header>`'ni hech qayerda haqiqatan ishlatmasa ham, havola qilingan komponentning tree-shaking qilinishiga toʻsqinlik qiladi.
Agar `LibHeader`'ning kodi, shabloni va stillari birgalikda juda katta boʻlib ketsa, uni keraksiz ravishda qoʻshish klient ilovasining hajmini sezilarli darajada oshirishi mumkin.

## Yengil inyeksiya tokeni namunasini qachon ishlatish kerak {#when-to-use-the-lightweight-injection-token-pattern}

Tree-shaking muammosi komponent inyeksiya tokeni sifatida ishlatilganda yuzaga keladi.
Bu ikki holatda yuz berishi mumkin:

- Token [kontent soʻrovining](guide/components/queries#content-queries) qiymat pozitsiyasida ishlatiladi.
- Token `inject` funksiyasi bilan ishlatiladi.

Quyidagi misolda `CustomOther` tokenining ikkala ishlatilishi ham `CustomOther`'ning saqlanib qolishiga sabab boʻladi va u ishlatilmaganda tree-shaking qilinishiga toʻsqinlik qiladi:

```ts {highlight: [[2],[4]]}
class App {
  private readonly other = inject(CustomOther, {optional: true});

  readonly header = contentChild(CustomOther);
}
```

Faqat tur koʻrsatkichi sifatida ishlatiladigan tokenlar JavaScript'ga konvertatsiya qilinganda olib tashlansa-da, bogʻliqliklarni inyeksiya qilish uchun ishlatiladigan barcha tokenlar ishga tushirish vaqtida kerak boʻladi.
`inject(CustomOther)` ishlatilganda `CustomOther` qiymat argumenti sifatida uzatiladi.
Token endi qiymat pozitsiyasida boʻladi, bu esa tree-shaker'ning havolani saqlab qolishiga sabab boʻladi.

HELPFUL: Kutubxonalar barcha servislar uchun [tree-shaking qilinadigan provider'lardan](guide/di/defining-dependency-providers) foydalanishi va bogʻliqliklarni komponentlar yoki modullarda emas, balki root darajasida taqdim etishi kerak.

## Yengil inyeksiya tokenlaridan foydalanish {#using-lightweight-injection-tokens}

Yengil inyeksiya tokeni dizayn namunasi kichik abstrakt klassni inyeksiya tokeni sifatida ishlatish va haqiqiy realizatsiyani keyingi bosqichda taqdim etishdan iborat.
Abstrakt klass saqlanib qoladi, tree-shaking qilinmaydi, lekin u kichik va ilova hajmiga sezilarli taʼsir koʻrsatmaydi.

Quyidagi misol bu `LibHeader` uchun qanday ishlashini koʻrsatadi:

```ts {highlight: [[1],[5], [15]]}
abstract class LibHeaderToken {}

@Component({
  selector: 'lib-header',
  providers: [{provide: LibHeaderToken, useExisting: LibHeader}],
  …,
})
class LibHeader extends LibHeaderToken {}

@Component({
  selector: 'lib-card',
  …,
})
class LibCard {
  readonly header = contentChild(LibHeaderToken);
}
```

Bu misolda `LibCard` realizatsiyasi endi `LibHeader`'ga na tur pozitsiyasida, na qiymat pozitsiyasida murojaat qiladi.
Bu `LibHeader`'ning toʻliq tree-shaking qilinishiga imkon beradi.
`LibHeaderToken` saqlanib qoladi, lekin u aniq realizatsiyasi boʻlmagan shunchaki klass eʼloni.
U kichik va kompilyatsiyadan keyin saqlanib qolganda ilova hajmiga sezilarli taʼsir qilmaydi.

Buning oʻrniga `LibHeader`'ning oʻzi abstrakt `LibHeaderToken` klassini amalga oshiradi.
Bu tokenni komponent taʼrifida provider sifatida xavfsiz ishlatishingiz mumkin, bu Angular'ga aniq turni toʻgʻri inyeksiya qilish imkonini beradi.

Xulosa qilib aytganda, yengil inyeksiya tokeni namunasi quyidagilardan iborat:

1. Abstrakt klass sifatida ifodalangan yengil inyeksiya tokeni.
2. Abstrakt klassni amalga oshiruvchi komponent taʼrifi.
3. `contentChild` yoki `contentChildren` yordamida yengil namunani inyeksiya qilish.
4. Yengil inyeksiya tokenini realizatsiya bilan bogʻlovchi, yengil inyeksiya tokeni realizatsiyasidagi provider.

### API taʼrifi uchun yengil inyeksiya tokenidan foydalanish {#use-the-lightweight-injection-token-for-api-definition}

Yengil inyeksiya tokenini inyeksiya qiladigan komponentga inyeksiya qilingan klassdagi metodni chaqirish kerak boʻlishi mumkin.
Token endi abstrakt klass. Inyeksiya qilinadigan komponent oʻsha klassni amalga oshirgani uchun siz abstrakt yengil inyeksiya tokeni klassida abstrakt metodni ham eʼlon qilishingiz kerak.
Metodning realizatsiyasi, uning barcha kod yuki bilan birga, tree-shaking qilinishi mumkin boʻlgan inyeksiya qilinadigan komponentda joylashadi.
Bu ota komponentga bola komponent mavjud boʻlsa, u bilan tur jihatidan xavfsiz tarzda muloqot qilish imkonini beradi.

Masalan, `LibCard` endi `LibHeader` oʻrniga `LibHeaderToken`'ni soʻraydi.
Quyidagi misol namuna `LibCard`'ga `LibHeader`'ga haqiqatan murojaat qilmasdan `LibHeader` bilan qanday muloqot qilish imkonini berishini koʻrsatadi:

```ts {highlight: [[2],[7],[11],[19]]}
abstract class LibHeaderToken {
  abstract doSomething(): void;
}

@Component({
  selector: 'lib-header',
  providers: [{provide: LibHeaderToken, useExisting: LibHeader}],
})
class LibHeader extends LibHeaderToken {
  doSomething(): void {
    // Concrete implementation of `doSomething`
  }
}

@Component({
  selector: 'lib-card',
})
class LibCard implements AfterContentInit {
  readonly header = contentChild(LibHeaderToken);

  ngAfterContentInit(): void {
    if (this.header() !== undefined) {
      this.header()!.doSomething();
    }
  }
}
```

Bu misolda ota komponent bola komponentni olish uchun tokenni soʻraydi va agar u mavjud boʻlsa, natijaviy komponent havolasini saqlaydi.
Boladagi metodni chaqirishdan oldin ota komponent bola komponent mavjudligini tekshiradi.
Agar bola komponent tree-shaking qilingan boʻlsa, unga ishga tushirish vaqtida havola boʻlmaydi va uning metodi chaqirilmaydi.

### Yengil inyeksiya tokeningizni nomlash {#naming-your-lightweight-injection-token}

Yengil inyeksiya tokenlari faqat komponentlar bilan foydali.
[Angular uslub qoʻllanmasi](style-guide) komponentlarni `Component` qoʻshimchasisiz nomlashni tavsiya qiladi.
`LibHeader` misoli shu konvensiyaga amal qiladi.

Komponent va uning tokeni oʻrtasidagi bogʻliqlikni saqlab qolgan holda, ularni bir-biridan farqlashingiz kerak.
Tavsiya etilgan uslub — yengil inyeksiya tokenlaringizni nomlash uchun komponentning asosiy nomini `Token` qoʻshimchasi bilan ishlatish: `LibHeaderToken`.
