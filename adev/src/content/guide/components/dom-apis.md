# DOM API'laridan foydalanish

TIP: Bu qoʻllanma siz [Asosiy tushunchalar qoʻllanmasini](essentials) allaqachon oʻqib chiqqan deb hisoblaydi. Agar Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

Angular DOM'ni yaratish, yangilash va olib tashlash ishlarining koʻp qismini siz uchun bajaradi. Biroq kamdan-kam hollarda komponentning DOM'i bilan bevosita ishlashingiz kerak boʻlishi mumkin. Komponentlar oʻzining host elementiga havola olish uchun ElementRef'ni inyeksiya qilishi mumkin:

```ts
@Component(/* ... */)
export class ProfilePhoto {
  constructor() {
    const elementRef = inject(ElementRef);
    console.log(elementRef.nativeElement);
  }
}
```

`nativeElement` xususiyati host [Element](https://developer.mozilla.org/docs/Web/API/Element) nusxasiga havola qiladi.

Angular sahifani render qilishni tugatganda ishga tushadigan **render callback**'ni roʻyxatdan oʻtkazish uchun Angular'ning `afterEveryRender` va `afterNextRender` funksiyalaridan foydalanishingiz mumkin.

```ts
@Component(/* ... */)
export class ProfilePhoto {
  constructor() {
    const elementRef = inject(ElementRef);
    afterEveryRender(() => {
      // Focus the first input element in this component.
      elementRef.nativeElement.querySelector('input')?.focus();
    });
  }
}
```

`afterEveryRender` va `afterNextRender` _inyeksiya kontekstida_ (injection context), odatda komponentning konstruktorida chaqirilishi shart.

**Imkon qadar DOM'ni bevosita oʻzgartirishdan saqlaning.** Har doim DOM tuzilmasini komponent shablonlarida ifodalashni va oʻsha DOM'ni bogʻlashlar orqali yangilashni afzal koʻring.

**Render callback'lar server tomonida render qilish yoki build vaqtidagi oldindan render qilish (pre-rendering) jarayonida hech qachon ishga tushmaydi.**

**Angular'ning boshqa hayot sikli hook'lari ichida DOM'ni hech qachon bevosita oʻzgartirmang**. Angular render callback'lardan tashqari hech qanday nuqtada komponent DOM'ining toʻliq render qilinganini kafolatlamaydi. Bundan tashqari, boshqa hayot sikli hook'lari davomida DOM'ni oʻqish yoki oʻzgartirish [layout thrashing](https://web.dev/avoid-large-complex-layouts-and-layout-thrashing) hodisasini keltirib chiqarib, sahifa unumdorligiga salbiy taʼsir koʻrsatishi mumkin.

## Komponent renderer'idan foydalanish {#using-a-components-renderer}

Komponentlar Angular'ning boshqa imkoniyatlari bilan bogʻliq boʻlgan maʼlum DOM oʻzgartirishlarini bajarish uchun `Renderer2` nusxasini inyeksiya qilishi mumkin.

Komponentning `Renderer2`'si tomonidan yaratilgan har qanday DOM elementlari oʻsha komponentning [stil inkapsulyatsiyasida](guide/components/styling#style-scoping) ishtirok etadi.

Baʼzi `Renderer2` API'lari Angular'ning animatsiya tizimi bilan ham bogʻlangan. Sintetik animatsiya xususiyatlarini yangilash uchun `setProperty` metodidan, sintetik animatsiya hodisalari uchun hodisa tinglovchilarini qoʻshish uchun esa `listen` metodidan foydalanishingiz mumkin. Batafsil maʼlumot uchun [Animatsiyalar](guide/animations) qoʻllanmasiga qarang.

Bu ikki tor holatdan tashqari, `Renderer2` va native DOM API'laridan foydalanish oʻrtasida farq yoʻq. `Renderer2` API'lari server tomonida render qilish yoki build vaqtidagi oldindan render qilish kontekstlarida DOM'ni oʻzgartirishni qoʻllab-quvvatlamaydi.

## DOM API'larini qachon ishlatish kerak {#when-to-use-dom-apis}

Angular render qilish bilan bogʻliq masalalarning koʻp qismini hal qilsa-da, baʼzi xatti-harakatlar hali ham DOM API'laridan foydalanishni talab qilishi mumkin. Keng tarqalgan holatlardan baʼzilari:

- Element fokusini boshqarish
- Element geometriyasini oʻlchash, masalan, `getBoundingClientRect` yordamida
- Elementning matn tarkibini oʻqish
- [`MutationObserver`](https://developer.mozilla.org/docs/Web/API/MutationObserver),
  [`ResizeObserver`](https://developer.mozilla.org/docs/Web/API/ResizeObserver) yoki
  [`IntersectionObserver`](https://developer.mozilla.org/docs/Web/API/Intersection_Observer_API) kabi
  native kuzatuvchilarni (observers) sozlash.

DOM elementlarini qoʻshish, olib tashlash va oʻzgartirishdan saqlaning. Xususan, **elementning `innerHTML` xususiyatini hech qachon bevosita oʻrnatmang**, chunki bu ilovangizni [saytlararo skripting (XSS) hujumlariga](https://developer.mozilla.org/docs/Glossary/Cross-site_scripting) zaif qilib qoʻyishi mumkin. Angular'ning shablon bogʻlashlari, jumladan `innerHTML` uchun bogʻlashlar, XSS hujumlaridan himoyalanishga yordam beradigan xavfsizlik choralarini oʻz ichiga oladi. Batafsil maʼlumot uchun [Xavfsizlik qoʻllanmasiga](best-practices/security) qarang.
