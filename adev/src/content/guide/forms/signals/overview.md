<docs-decorative-header title="Angular signallari bilan formalar" imgSrc="adev/src/assets/images/signals.svg"> <!-- markdownlint-disable-line -->
</docs-decorative-header>

Signal Forms — signallarning reaktiv asosiga qurilgan, Angular ilovalarida forma holatini boshqarish imkonini beruvchi kutubxona. Avtomatik ikki tomonlama bogʻlash, tiplar jihatidan xavfsiz maydonlarga murojaat va sxemaga asoslangan validatsiya bilan Signal Forms sizga ishonchli formalar yaratishga yordam beradi.

TIP: Signal Forms bilan tez tanishish uchun [Signal Forms asoslari qoʻllanmasiga](essentials/signal-forms) qarang.

## Nega Signal Forms? {#why-signal-forms}

Veb-ilovalarda formalar yaratish bir-biri bilan bogʻliq bir nechta vazifani boshqarishni oʻz ichiga oladi: maydon qiymatlarini kuzatish, foydalanuvchi kiritgan maʼlumotlarni tekshirish, xato holatlarini qayta ishlash va UI'ni maʼlumotlar modelingiz bilan sinxron holda saqlash. Bu vazifalarni alohida-alohida boshqarish shablon kod (boilerplate) va murakkablikni keltirib chiqaradi.

Signal Forms bu muammolarni quyidagicha hal qiladi:

- **Holatni avtomatik sinxronlash** - Forma maʼlumotlar modelini bogʻlangan forma maydonlari bilan avtomatik sinxronlaydi
- **Tiplar xavfsizligini taʼminlash** - UI kontrollaringiz va maʼlumotlar modeli oʻrtasida toʻliq tiplar jihatidan xavfsiz sxemalar va bogʻlashlarni qoʻllab-quvvatlaydi
- **Validatsiya logikasini markazlashtirish** - Barcha validatsiya qoidalarini validatsiya sxemasi yordamida bir joyda aniqlang

Signal Forms signallar bilan qurilgan yangi ilovalarda eng yaxshi ishlaydi. Agar reaktiv formalardan foydalanadigan mavjud ilova bilan ishlayotgan boʻlsangiz, reaktiv formalar ishonchli tanlov boʻlib qolaveradi.

NOTE: Agar siz shablon formalari yoki reaktiv formalardan oʻtayotgan boʻlsangiz, [qiyoslash qoʻllanmasi](guide/forms/signals/comparison) sizni qiziqtirishi mumkin.

## Talablar {#prerequisites}

Signal Forms uchun quyidagilar talab qilinadi:

- Angular v21 yoki undan yuqori versiya

## Oʻrnatish {#setup}

Signal Forms allaqachon `@angular/forms` paketiga kiritilgan. Kerakli funksiya va direktivalarni `@angular/forms/signals`'dan import qiling:

```ts
import {form, FormField, required, email} from '@angular/forms/signals';
```

`FormField` direktivi forma maydonlarini HTML input'larga bogʻlaydigan har bir komponentga import qilinishi kerak:

```ts
@Component({
  // ...
  imports: [FormField],
})
```

## Keyingi qadamlar {#next-steps}

Signal Forms qanday ishlashi haqida koʻproq bilish uchun quyidagi qoʻllanmalarga qarang:

<docs-pill-row>
  <docs-pill href="essentials/signal-forms" title="Signal forms asoslari" />
  <docs-pill href="guide/forms/signals/models" title="Forma modellari" />
  <docs-pill href="guide/forms/signals/model-design" title="Forma modelingizni loyihalash" />
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <docs-pill href="guide/forms/signals/custom-controls" title="Maxsus kontrollar" />
  <docs-pill href="guide/forms/signals/comparison" title="Boshqa forma tizimlari bilan qiyoslash" />
</docs-pill-row>
