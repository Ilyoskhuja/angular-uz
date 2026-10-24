# Komponentlarga stillar berish

TIP: Bu qoʻllanma siz [Asoslar qoʻllanmasini](essentials) allaqachon oʻqib chiqqan deb hisoblaydi. Agar Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Komponentlar ixtiyoriy ravishda oʻsha komponentning DOM'iga qoʻllaniladigan CSS stillarini oʻz ichiga olishi mumkin:

```angular-ts {highlight:[4]}
@Component({
  selector: 'profile-photo',
  template: `<img src="profile-photo.jpg" alt="Your profile photo" />`,
  styles: `
    img {
      border-radius: 50%;
    }
  `,
})
export class ProfilePhoto {}
```

Shuningdek, stillaringizni alohida fayllarda yozishni ham tanlashingiz mumkin:

```angular-ts {highlight:[4]}
@Component({
  selector: 'profile-photo',
  templateUrl: 'profile-photo.html',
  styleUrl: 'profile-photo.css',
})
export class ProfilePhoto {}
```

Angular komponentingizni kompilyatsiya qilganda, bu stillar komponentingizning JavaScript chiqishi bilan birga
chiqariladi. Bu komponent stillari JavaScript modul tizimida ishtirok etishini anglatadi. Angular komponentini
render qilganingizda, freymvork unga tegishli stillarni avtomatik ravishda qoʻshadi, hatto komponent
lazy loading orqali yuklanganda ham.

Angular CSS chiqaradigan har qanday vosita bilan ishlaydi,
jumladan [Sass](https://sass-lang.com), [Less](https://lesscss.org)
va [Stylus](https://stylus-lang.com) bilan.

## Stillar qamrovi {#style-scoping}

Har bir komponentda freymvork komponent stillarining qamrovini qanday belgilashini aniqlaydigan **view inkapsulyatsiyasi**
sozlamasi mavjud. View inkapsulyatsiyasining toʻrtta rejimi bor: `Emulated`, `ShadowDom`, `ExperimentalIsolatedShadowDom` va `None`.
Rejimni `@Component` dekoratorida koʻrsatishingiz mumkin:

```angular-ts {highlight:[3]}
@Component({
  ...,
  encapsulation: ViewEncapsulation.None,
})
export class ProfilePhoto { }
```

### ViewEncapsulation.Emulated

Sukut boʻyicha Angular emulyatsiya qilingan inkapsulyatsiyadan foydalanadi, shunda komponent stillari faqat oʻsha
komponent shablonida aniqlangan elementlarga qoʻllaniladi. Bu rejimda freymvork har bir komponent nusxasi uchun
noyob HTML atributi yaratadi, bu atributni komponent shablonidagi elementlarga qoʻshadi va
komponent stillarida aniqlangan CSS selektorlariga shu atributni kiritadi.

Bu rejim komponent stillarining tashqariga chiqib ketmasligini va boshqa komponentlarga taʼsir qilmasligini taʼminlaydi. Biroq,
komponentdan tashqarida aniqlangan global stillar emulyatsiya qilingan inkapsulyatsiyali komponent ichidagi
elementlarga hali ham taʼsir qilishi mumkin.

Emulyatsiya rejimida Angular
[`:host`](https://developer.mozilla.org/docs/Web/CSS/:host) psevdo-klassini qoʻllab-quvvatlaydi.
[`:host-context()`](https://developer.mozilla.org/docs/Web/CSS/:host-context) psevdo-klassi zamonaviy brauzerlarda
eskirgan (deprecated) boʻlsa-da, Angular kompilyatori uni toʻliq qoʻllab-quvvatlaydi. Ikkala psevdo-klassdan ham
tabiiy (native) [Shadow DOM](https://developer.mozilla.org/docs/Web/Web_Components/Using_shadow_DOM)'ga
tayanmasdan foydalanish mumkin.
Kompilyatsiya vaqtida freymvork bu psevdo-klasslarni atributlarga aylantiradi, shuning uchun ish vaqtida u bu tabiiy
psevdo-klasslarning qoidalariga (masalan, brauzer mosligi, spetsifiklik) boʻysunmaydi. Angular'ning
emulyatsiya qilingan inkapsulyatsiya rejimi Shadow DOM bilan bogʻliq boshqa psevdo-klasslarni, masalan
`::shadow` yoki `::part` ni qoʻllab-quvvatlamaydi.

#### `::ng-deep`

Angular'ning emulyatsiya qilingan inkapsulyatsiya rejimi maxsus psevdo-klass — `::ng-deep` ni qoʻllab-quvvatlaydi.
**Angular jamoasi `::ng-deep` dan yangi foydalanishni qatʼiy tavsiya etmaydi**. Bu API'lar faqat
orqaga moslik uchun saqlanib qolgan.

Selektorda `::ng-deep` boʻlsa, Angular selektorning shu nuqtasidan keyin view inkapsulyatsiyasi chegaralarini qoʻllashni toʻxtatadi. Selektorning `::ng-deep` dan keyin keladigan har qanday qismi komponent shablonidan tashqaridagi elementlarga mos kelishi mumkin.

Masalan:

- `p a` kabi CSS qoida selektori emulyatsiya qilingan inkapsulyatsiyada `<p>` elementining avlodi boʻlgan `<a>` elementlariga mos keladi,
  bunda ikkalasi ham komponentning oʻz shablonida boʻlishi kerak.

- `::ng-deep p a` kabi selektor ilovaning istalgan joyidagi `<a>` elementlariga — ilovaning istalgan joyidagi `<p>` elementining avlodlariga mos keladi.

  Bu amalda uni global stil kabi ishlashga majbur qiladi.

- `p ::ng-deep a` da Angular `<p>` elementining komponentning oʻz shablonidan boʻlishini talab qiladi, lekin `<a>` elementi ilovaning istalgan joyida boʻlishi mumkin.

  Demak, amalda `<a>` elementi komponent shablonida yoki uning proyeksiya qilingan yoxud bola kontentining istalgan joyida boʻlishi mumkin.

- `:host ::ng-deep p a` bilan `<a>` ham, `<p>` elementlari ham komponentning host elementining avlodlari boʻlishi shart.

  Ular komponent shablonidan yoki uning bola komponentlarining view'laridan kelishi mumkin, lekin ilovaning boshqa joyidan emas.

### ViewEncapsulation.ShadowDom

Bu rejim komponent ichidagi stillar qamrovini
[veb standarti boʻlgan Shadow DOM API](https://developer.mozilla.org/docs/Web/Web_Components/Using_shadow_DOM) yordamida belgilaydi.
Bu rejim yoqilganda Angular komponentning host elementiga shadow root biriktiradi va komponent shabloni
hamda stillarini tegishli shadow daraxtiga render qiladi.

Shadow daraxti ichidagi stillar oʻsha shadow daraxtidan tashqaridagi elementlarga taʼsir qila olmaydi.

Biroq `ShadowDom` inkapsulyatsiyasini yoqish stillar qamrovidan koʻra koʻproq narsaga taʼsir qiladi. Komponentni
shadow daraxtida render qilish hodisalarning tarqalishiga,
[`<slot>` API](https://developer.mozilla.org/docs/Web/Web_Components/Using_templates_and_slots) bilan oʻzaro taʼsirga
va brauzer dasturchi vositalarining elementlarni qanday koʻrsatishiga taʼsir qiladi. Bu opsiyani yoqishdan oldin ilovangizda
Shadow DOM'dan foydalanishning toʻliq oqibatlarini doimo tushunib oling.

### ViewEncapsulation.ExperimentalIsolatedShadowDom

Yuqoridagidek ishlaydi, faqat bu rejim komponent shablonidagi elementlarga _faqat_ oʻsha komponentning stillari
qoʻllanilishini qatʼiy kafolatlaydi. Global stillar shadow daraxtidagi elementlarga taʼsir qila olmaydi va shadow
daraxti ichidagi stillar oʻsha shadow daraxtidan tashqaridagi elementlarga taʼsir qila olmaydi.

### ViewEncapsulation.None

Bu rejim komponent uchun stillar inkapsulyatsiyasini butunlay oʻchiradi. Komponent bilan bogʻliq har qanday stillar
global stillar kabi ishlaydi.

NOTE: `Emulated` va `ShadowDom` rejimlarida Angular komponentingiz stillarining tashqaridan kelgan stillarni har doim bekor qilishini 100% kafolatlamaydi.
Toʻqnashuv yuz berganda bu stillar komponentingiz stillari bilan bir xil spetsifiklikka ega deb hisoblanadi.

## Shablonlarda stillarni aniqlash {#defining-styles-in-templates}

Qoʻshimcha stillarni aniqlash uchun komponent shablonida `<style>` elementidan foydalanishingiz mumkin.
Bu tarzda aniqlangan stillarga komponentning view inkapsulyatsiyasi rejimi qoʻllaniladi.

Angular style elementlari ichida bogʻlashlarni qoʻllab-quvvatlamaydi.

## Tashqi stil fayllariga murojaat qilish {#referencing-external-style-files}

Komponent shablonlari CSS fayllariga murojaat qilish uchun
[`<link>` elementidan](https://developer.mozilla.org/docs/Web/HTML/Element/link)
foydalanishi mumkin. Bundan tashqari, CSS'ingiz CSS fayllariga murojaat qilish uchun
[`@import` at-qoidasidan](https://developer.mozilla.org/docs/Web/CSS/@import)
foydalanishi mumkin. Angular bu murojaatlarni _tashqi_ stillar sifatida koʻradi. Tashqi stillarga
emulyatsiya qilingan view inkapsulyatsiyasi taʼsir qilmaydi.

## CSS maxsus xususiyatlarini nomlar fazosiga ajratish {#namespacing-css-custom-properties}

Angular komponent stillaringiz eʼlon qiladigan va oʻqiydigan CSS maxsus xususiyatlariga (CSS oʻzgaruvchilari deb ham ataladi)
prefiks qoʻshishi mumkin. Maxsus xususiyatlar DOM daraxti boʻylab pastga meros boʻlib oʻtadi, shuning uchun ilovangizdan
tashqaridagi biror narsa ajdod elementda `--primary-color` kabi maxsus xususiyatni aniqlasa,
komponentlaringiz oʻsha qiymatni oʻqiydi. Bu ilovangiz sahifani boshqa ilova yoki siz nazorat qilmaydigan
markup bilan boʻlishganda muhim. Angular siz soʻramaguningizcha maxsus xususiyatlarni nomlar fazosiga ajratmaydi
va oʻz sahifasiga egalik qiladigan ilovaga nomlar fazosiga ajratish kerak emas.

Komponent stillaringizdagi maxsus xususiyatlar qamrovini ilovangiz bilan cheklash uchun ilovangizning
provider'lariga [`provideCssVarNamespacing`](api/platform-browser/provideCssVarNamespacing) ni qoʻshing.
U nomlar fazosi sifatida ilovaning [`APP_ID`](api/core/APP_ID) qiymatidan foydalanadi:

```ts {header: "app.config.ts"}
import {APP_ID, ApplicationConfig} from '@angular/core';
import {provideCssVarNamespacing} from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [{provide: APP_ID, useValue: 'my-app'}, provideCssVarNamespacing()],
};
```

Angular komponent stillaringizdagi maxsus xususiyatlarga oʻsha nomlar fazosi va undan keyin pastki chiziqdan iborat
prefiks qoʻyadi, shunda `--primary-color` `--my-app_primary-color` ga aylanadi. Prefiks eʼlonlarga,
`var()` murojaatlariga, `@property` qoidalariga va `[style.--primary-color]` kabi stil bogʻlashlariga,
jumladan komponent oʻzining `host` obyektida eʼlon qiladigan stil bogʻlashlariga qoʻllaniladi.

Siz oʻrnatmaguningizcha `APP_ID` qiymati `ng` boʻladi, shuning uchun sahifadagi har bir ilovaga oʻz `APP_ID` sini bering.
Aks holda ilovalar bir xil prefiksga ega boʻlib, yana toʻqnashadi. Ilova id'sidan farq qiladigan nomlar fazosidan
foydalanish uchun uni `provideCssVarNamespacing` ga uzating. Angular pastki chiziqni oʻzi qoʻshadi:
`provideCssVarNamespacing('my-app_')` natijasida `--my-app__primary-color` hosil boʻladi.

Angular komponentga kompilyatsiya qiladigan stillarni nomlar fazosiga ajratadi: komponentning `styles` va `styleUrl`'i,
shablonidagi [`<style>` elementida yozgan](#defining-styles-in-templates) stillaringiz,
shabloni nisbiy `<link rel="stylesheet">` orqali murojaat qiladigan stil jadvallari va
`ViewEncapsulation.None` dan foydalanadigan komponentning stillari. Angular brauzer ish vaqtida yuklaydigan stil jadvalini,
masalan build konfiguratsiyangizda roʻyxatga olingan global stil jadvalini yoki build'ingiz inline qilmaydigan
[tashqi stilni](#referencing-external-style-files) nomlar fazosiga ajratmaydi.

Nomlar fazosiga ajratish Angular kompilyatsiya qiladigan har bir komponentga, jumladan siz oʻrnatgan kutubxonalarning
komponentlariga ham qoʻllaniladi. Kutubxona stillari global stil jadvali aniqlagan maxsus xususiyatni, masalan
mavzu (theme) xususiyatlarini oʻqiganda, murojaat endi mos kelmaydi, brauzer `var()` ning zaxira variantidan (fallback),
agar u mavjud boʻlsa, aks holda
[xususiyatning meros qilib olingan yoki boshlangʻich qiymatidan](https://www.w3.org/TR/css-variables-1/#invalid-variables)
foydalanadi va hech narsa xato haqida xabar bermaydi. Mavjud ilovada nomlar fazosiga ajratishni yoqishdan oldin
global stil jadvallaringiz va komponentlaringiz oʻrtasida kesishadigan maxsus xususiyatlarni
koʻrib chiqing.

IMPORTANT: Angular maxsus xususiyat nomlarini faqat oʻzi kompilyatsiya qiladigan stillar va bogʻlashlarda qayta yozadi.
Boshqa hamma joyda siz yozgan nom saqlanib qoladi va hech narsa nomuvofiqlik haqida xabar bermaydi.

Angular quyidagilarda nomni qayta yozmaydi:

- `style="--primary-color: red"` kabi statik style atributlari, jumladan komponentning `host` obyektidagi
  `style` yozuvi.
- `[style]="{'--primary-color': color}"`, `[style]="'--primary-color: red'"` va `ngStyle` kabi obyekt va
  satr koʻrinishidagi stil bogʻlashlari, jumladan komponentning `host` obyektidagi `[style]`
  yozuvi.
- Bogʻlash qiymati ichidagi maxsus xususiyat nomlari, masalan
  `[style.border-color]="'var(--primary-color)'"`.
- `Renderer2.setStyle` chaqiruvlari.

Bularning har biri nomlar fazosiga ajratilgan stillaringiz endi oʻqimaydigan xususiyatni hosil qiladi. Bu nomlarni
[Nomlar fazosiga ajratilgan xususiyatlardan TypeScript'da foydalanish](#using-namespaced-properties-in-typescript)
boʻlimida tavsiflanganidek, oʻzingiz nomlar fazosiga ajrating.

### Nomlar fazosiga ajratishdan voz kechish {#opting-out-of-namespacing}

Angular nomlar fazosiga ajratmaydigan maxsus xususiyatni, masalan global stil jadvalida aniqlanganini, eʼlon qilish
yoki oʻqish uchun uning nomi oldiga `--global--` prefiksini qoʻying. Angular `--global` ni olib tashlaydi va
qolgan `--` hamda nomning qolgan qismini oʻzgarishsiz qoldiradi:

```css
:host {
  /* Declares --accent-color and reads --brand-color, not --my-app_brand-color. */
  --global--accent-color: navy;
  color: var(--global--brand-color);
}
```

`global` dan keyin ikkita defis yozing. `--global-brand-color` dagi kabi bitta defis voz kechishni anglatmaydi
va Angular bu nomni boshqa har qanday nom kabi nomlar fazosiga ajratadi. `--global-` dan keyin ikkinchi defisdan boshqa
narsa keladigan nomlardan saqlaning; kelajakdagi major versiyada ularni build vaqtida rad etish rejalashtirilgan.
Angular `--global` ni har bir ilovada, jumladan hech qachon nomlar fazosini sozlamagan ilovalarda ham
olib tashlaydi.

### Nomlar fazosiga ajratilgan xususiyatlardan TypeScript'da foydalanish {#using-namespaced-properties-in-typescript}

Angular siz uchun nomlar fazosiga ajratadigan `[style.--primary-color]` kabi stil bogʻlashini afzal koʻring. Buning oʻrniga
DOM API orqali ishlaganingizda, stillaringizda yozgan nomni, boshidagi `--` bilan birga,
[`CssVarNamespacer`](api/platform-browser/CssVarNamespacer) ga uzating:

```angular-ts {header: "profile-photo.ts"}
import {Component, ElementRef, inject} from '@angular/core';
import {CssVarNamespacer} from '@angular/platform-browser';

@Component({
  selector: 'profile-photo',
  template: `<img src="profile-photo.jpg" alt="Your profile photo" />`,
  styles: `
    img {
      border: 2px solid var(--primary-color);
    }
  `,
})
export class ProfilePhoto {
  private readonly host: HTMLElement = inject(ElementRef).nativeElement;
  private readonly cssVarNamespacer = inject(CssVarNamespacer);

  setPrimaryColor(color: string): void {
    this.host.style.setProperty(this.cssVarNamespacer.namespace('--primary-color'), color);
  }
}
```

`--global--` bilan eʼlon qilgan xususiyat uchun oddiy nomdan foydalaning, chunki Angular ularni hech qachon nomlar
fazosiga ajratmaydi. Qolgan hamma narsa uchun ilova nomlar fazosini sozlamagan boʻlsa, `namespace` nomni oʻzgarishsiz
qaytaradi, shuning uchun kutubxona oʻz stillari eʼlon qiladigan maxsus xususiyatlar uchun uni chaqirishi mumkin.
