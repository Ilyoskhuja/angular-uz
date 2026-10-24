# Komponentning kengaytirilgan konfiguratsiyasi

TIP: Bu qoʻllanma siz [Asosiy tushunchalar qoʻllanmasini](essentials) allaqachon oʻqib chiqqan deb hisoblaydi. Agar Angular'da yangi boʻlsangiz, avval oʻshani oʻqing.

## ChangeDetectionStrategy {#changedetectionstrategy}

`@Component` dekoratori komponentning **oʻzgarishlarni aniqlash rejimini** (change detection mode) boshqaruvchi `changeDetection` opsiyasini qabul qiladi. Oʻzgarishlarni aniqlash rejimining ikkita varianti mavjud.

**`ChangeDetectionStrategy.Eager`/`Default`** — ixtiyoriy rejim. Bu rejimda Angular ilova miqyosida qandaydir faollik yuz bergan boʻlishi mumkin boʻlgan har safar komponentning DOM'i yangilanishga muhtojligini tekshiradi. Bunday tekshiruvni ishga tushiradigan faolliklarga foydalanuvchi harakatlari, tarmoq javoblari, taymerlar va boshqalar kiradi.

**`ChangeDetectionStrategy.OnPush`** — sukut boʻyicha strategiya (v22 dan boshlab). Bu rejim Angular bajarishi kerak boʻlgan tekshiruvlar hajmini kamaytiradi. Bu rejimda freymvork komponentning DOM'i yangilanishga muhtojligini faqat quyidagi hollarda tekshiradi:

- Komponent input'i shablondagi bogʻlash natijasida oʻzgarganda, yoki
- Bu komponentdagi hodisa tinglovchisi ishga tushganda
- Komponent `ChangeDetectorRef.markForCheck` yoki uni oʻrab oluvchi `AsyncPipe` kabi biror narsa orqali tekshirish uchun aniq belgilanganda.

Bundan tashqari, OnPush komponenti tekshirilganda Angular ilova daraxti boʻylab yuqoriga koʻtarilib, uning barcha ajdod komponentlarini _ham_ tekshiradi.

## PreserveWhitespaces {#preservewhitespaces}

Sukut boʻyicha Angular shablonlardagi ortiqcha boʻsh joylarni, koʻpincha yangi qatorlar va chekinishlardan (indentation) kelib chiqadiganlarini, olib tashlaydi va qisqartiradi. Komponent metadatasida `preserveWhitespaces` qiymatini aniq `true` ga oʻrnatib, bu sozlamani oʻzgartirishingiz mumkin.

## Maxsus element sxemalari {#custom-element-schemas}

Sukut boʻyicha Angular nomaʼlum HTML elementiga duch kelganda xato tashlaydi. Komponent metadatasidagi `schemas` xususiyatiga `CUSTOM_ELEMENTS_SCHEMA`'ni qoʻshib, komponent uchun bu xatti-harakatni oʻchirib qoʻyishingiz mumkin.

```angular-ts
import {Component, CUSTOM_ELEMENTS_SCHEMA} from '@angular/core';

@Component({
  ...,
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: '<some-unknown-component />'
})
export class ComponentWithCustomElements { }
```

Angular shuningdek istalgan element va istalgan xususiyatga ruxsat beruvchi `NO_ERRORS_SCHEMA`'ni ham taqdim etadi.
