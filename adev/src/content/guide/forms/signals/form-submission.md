# Formani yuborish

Foydalanuvchi formani yuborganda, ilovangiz odatda bir vaqtning oʻzida bir nechta masalani hal qilishi kerak boʻladi: validatsiya xatolarini koʻrsatish, takroriy yuborishning oldini olish, maʼlumotlarni serverga joʻnatish va boshqalar. Bularning har birini qoʻlda bajarish zerikarli va xatolarga moyil boʻlishi mumkin.

Signal Forms formani yuborish hayot siklini boshqarishga yordam beradigan `submit()` funksiyasini taqdim etadi. Ushbu qoʻllanma undan qanday foydalanishni koʻrsatib beradi.

## `submit()` nima qiladi? {#what-does-submit-do}

`submit()` funksiyasi maʼlum bir ketma-ketlikni bajaradi:

1. **Interaktiv maydonlarni tegilgan (touched) deb belgilaydi** — Xatolarni faqat tegilgandan keyin koʻrsatadigan maydonlar endi oʻz validatsiya xatolarini koʻrsatadi. Yashirin, oʻchirilgan va faqat oʻqish uchun maydonlar oʻtkazib yuboriladi.
1. **Validatsiyani tekshiradi** — Agar biror validatsiya qoidasi bajarilmagan boʻlsa, yuborish toʻxtaydi va `action` funksiyasi ishga tushmaydi.
1. **Action'ni bajaradi** — `action` funksiyasi formaning joriy qiymati bilan bajariladi. U ishlayotgan vaqtda `submitting()` `true` qaytaradi.
1. **Natijani qayta ishlaydi** — Agar action xatolar qaytarsa, ular oʻz maqsadli maydonlariga yoʻnaltiriladi. Agar u hech narsa qaytarmasa, yuborish muvaffaqiyatli deb hisoblanadi.

`submit()` funksiyasi `Promise<boolean>` qaytaradi: action xatosiz yakunlanganda u `true` ga, validatsiya muvaffaqiyatsiz boʻlganda, action xatolar qaytarganda yoki yuborish allaqachon davom etayotgan boʻlganda `false` ga yechiladi (resolve). Agar action xato tashlasa, promise shu xato bilan rad etiladi (reject).

## `FormRoot` bilan formani yuborishni sozlash {#setting-up-form-submission-with-formroot}

`submit()` funksiyasidan foydalanishning eng keng tarqalgan usuli — `FormRoot` direktivi orqali.

`FormRoot` direktivi `<form>` elementiga bogʻlanganda uchta narsani avtomatik bajaradi:

1. **[`novalidate`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form#novalidate) oʻrnatadi** — Brauzerning oʻrnatilgan validatsiyasini oʻchiradi, shunda validatsiyani uning oʻrniga Signal Forms boshqaradi
1. **Sukut boʻyicha xatti-harakatning oldini oladi** — Forma yuborilganda brauzerning boshqa sahifaga oʻtishini toʻxtatadi
1. **`submit()`'ni chaqiradi** — Agar forma `submission` opsiyasi bilan yaratilgan boʻlsa, foydalanuvchi formani yuborganda yuborish jarayonini ishga tushiradi

NOTE: `FormRoot` direktivi `form` elementiga `novalidate` atributini avtomatik oʻrnatadi. `FormRoot`'dan foydalanganda uni qoʻlda qoʻshishingiz shart emas.

`FormRoot` yuborish hodisasini qayta ishlaydi, lekin siz hali ham unga forma maʼlumotlari bilan _nima qilish kerakligini_ aytishingiz kerak. Buning uchun uchta narsa talab qilinadi:

1. Formangizni `FormRoot` direktiviga bogʻlang
1. `form()` funksiyasiga `submission` opsiyasini uzating
1. `submission` opsiyasi ichida yuborilgan maʼlumotlarni boshqaradigan `action` funksiyasini aniqlang

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, FormRoot, required} from '@angular/forms/signals';

@Component({
  selector: 'app-contact',
  imports: [FormField, FormRoot],
  template: `
    <form [formRoot]="contactForm">
      <label>
        Name
        <input [formField]="contactForm.name" />
      </label>

      <label>
        Email
        <input type="email" [formField]="contactForm.email" />
      </label>

      <button type="submit">Send</button>
    </form>
  `,
})
export class Contact {
  contactModel = signal({
    name: '',
    email: '',
  });

  contactForm = form(
    this.contactModel,
    (schemaPath) => {
      required(schemaPath.name);
      required(schemaPath.email);
    },
    {
      submission: {
        action: async (field) => {
          const result = await saveContact(field().value());
          if (result.ok) return;

          return {kind: 'serverError', message: 'Failed to submit form'};
        },
      },
    },
  );
}
```

`action` funksiyasi faqat hech bir validatsiya qoidasi buzilmagan holda ishga tushadi. Sukut boʻyicha kutilayotgan (pending) asinxron validatorlar yuborishni bloklamaydi (batafsil maʼlumot uchun [Validatsiya toʻsigʻini boshqarish](#controlling-validation-gating-with-ignorevalidators) boʻlimiga qarang). Action maydonlar daraxtini va `root` hamda `submitted` maydonlar daraxtlariga ega `detail` obyektini qabul qiladi; bu kichik formani (sub-form) yuborishda foydali.

Validatsiya muvaffaqiyatli oʻtgandan keyin ham action tarmoq xatosi yoki takroriy yozuv kabi holatlar tufayli muvaffaqiyatsiz boʻlishi mumkin. Bunday hollarda xato(lar)ni qaytarib, muvaffaqiyatsizlikni koʻrsatishingiz mumkin. Boshqa tomondan, muvaffaqiyatni bildirish uchun faqat `null` yoki `undefined` qaytarish yoki boʻsh `return` chaqirish kifoya.

## `submitting()` bilan yuborish holatini koʻrsatish {#showing-submission-state-with-submitting}

Formaning yuborish jarayonida ekanligini kuzatish kerak boʻlganda, Signal Forms `action` funksiyasi ishlayotgan vaqtda `true` qaytaradigan `submitting()` signalini taqdim etadi. Undan yuklanish indikatorlarini koʻrsatish yoki takroriy yuborishlarning oldini olish uchun yuborish tugmasini oʻchirishda foydalaning.

```angular-html
<button type="submit" [disabled]="contactForm().submitting()">
  @if (contactForm().submitting()) {
    Sending...
  } @else {
    Send
  }
</button>
```

`action` funksiyasi muvaffaqiyatli yakunlangach yoki xato qaytargach, `submitting()` signali avtomatik ravishda `false` holatiga qaytadi.

## Yuborish xatolarini boshqarish {#managing-submission-errors}

### Server xatolari {#server-errors}

`action` funksiyangiz server bilan aloqa qilganda, server muayyan maydonlarda koʻrinishi kerak boʻlgan xatolarni qaytarishi mumkin. Ushbu xatolarni maqsadli maydonlariga yoʻnaltirish uchun ularni `action`'dan qaytaring.

#### Yuborilgan maydondagi xatolar {#errors-on-the-submitted-field}

Sukut boʻyicha `action`'dan qaytarilgan xatolar yuborilgan maydonga (`submit()`'ga uzatgan maydonlar daraxtingizga) biriktiriladi:

```ts
action: async (field) => {
  const result = await saveContact(field().value());
  if (result.ok) return;

  return {kind: 'serverError', message: 'Failed to submit form'};
};
```

#### Muayyan maydonlardagi xatolar {#errors-on-specific-fields}

Xatoni muayyan maydonga yoʻnaltirmoqchi boʻlsangiz, oʻsha maydonga ishora qiluvchi `fieldTree` xususiyatini qoʻshing:

```ts
action: async (field) => {
  const result = await saveContact(field().value());
  if (result.ok) return;

  return {kind: 'taken', message: result.message, fieldTree: field.email};
};
```

#### Bir nechta xato {#multiple-errors}

Bir nechta maydonda xatolar haqida xabar bermoqchi boʻlsangiz, massiv qaytaring:

```ts
action: async (field) => {
  const result = await registerUser(field().value());
  if (result.ok) return;

  return result.errors.map((err: {field: string; message: string}) => ({
    kind: 'serverError',
    message: err.message,
    fieldTree: field[err.field as keyof typeof field],
  }));
};
```

### Yuborish xatolarini avtomatik tozalash {#auto-clearing-submission-errors}

Foydalanuvchi maydonni tahrirlaganda yuborish xatolari avtomatik tozalanadi. Agar `action` email maydonida xato qaytarsa, foydalanuvchi email qiymatini oʻzgartirishi bilan bu xato yoʻqoladi.

Bu reaktiv tarzda qayta hisoblanadigan validatsiya xatolaridan farq qiladi. Validatsiya qoidalari har bir oʻzgarishda qayta ishga tushadi va bir xil xatoni yana chiqarishi mumkin. Yuborish xatolari esa serverdan kelgan bir martalik natijalardir — bir marta tozalangach, forma qayta yuborilmaguncha ular yana paydo boʻlmaydi.

TIP: Yuborish xatolari maydonning `errors()` signalida validatsiya xatolari bilan birga koʻrinadi. Shablonda xatolarni koʻrsatish boʻyicha koʻrsatmalar uchun [Maydon holatini boshqarish qoʻllanmasiga](guide/forms/signals/field-state-management) qarang.

## `onInvalid` bilan notoʻgʻri yuborishlarni qayta ishlash {#handling-invalid-submissions-with-oninvalid}

Validatsiya muvaffaqiyatsiz boʻlganda `action` funksiyasi ishga tushmaydi. Agar muvaffaqiyatsiz yuborish urinishiga javob berishingiz kerak boʻlsa — masalan, birinchi xatoga aylantirish (scroll), toast koʻrsatish yoki notoʻgʻri maydonga fokus berish — `onInvalid` callback'idan foydalaning.

```ts
contactForm = form(
  this.contactModel,
  (schemaPath) => {
    required(schemaPath.name);
    required(schemaPath.email);
  },
  {
    submission: {
      action: async (field) => {
        await saveContact(field().value());
      },
      onInvalid: (field) => {
        const firstError = field().errorSummary()[0];
        firstError?.fieldTree().focusBoundControl();
      },
    },
  },
);
```

`onInvalid` callback'i `action` bilan bir xil `(field, detail)` parametrlarini qabul qiladi. U barcha interaktiv maydonlar tegilgan deb belgilangandan keyin ishga tushadi, shuning uchun u bajarilayotganda validatsiya xatolari UI'da allaqachon koʻrinib turadi.

## `ignoreValidators` bilan validatsiya toʻsigʻini boshqarish {#controlling-validation-gating-with-ignorevalidators}

Sukut boʻyicha `submit()` kutilayotgan validatorlarni eʼtiborsiz qoldiradi. Agar hech bir validator muvaffaqiyatsiz boʻlmagan boʻlsa, baʼzi asinxron validatorlar hali davom etayotgan boʻlsa ham action ishga tushadi. `ignoreValidators` opsiyasi bu xatti-harakatni boshqarish imkonini beradi.

| Qiymat      | Xatti-harakat                                                                                       |
| ----------- | --------------------------------------------------------------------------------------------------- |
| `'pending'` | Hech bir validator muvaffaqiyatsiz boʻlmasa, baʼzilari kutilayotgan boʻlsa ham yuboradi (sukut boʻyicha) |
| `'none'`    | Faqat barcha validatorlar oʻtganda yuboradi — kutilayotgan validatorlar yuborishni bloklaydi        |
| `'all'`     | Validatsiya holatidan qatʼi nazar har doim yuboradi                                                 |

```ts
contactForm = form(
  this.contactModel,
  (schemaPath) => {
    required(schemaPath.name);
    required(schemaPath.email);
  },
  {
    submission: {
      action: async (field) => {
        await saveContact(field().value());
      },
      ignoreValidators: 'none',
    },
  },
);
```

Formangizda asinxron validatorlar boʻlsa (masalan, foydalanuvchi nomining bandligini tekshirish) va yuborishdan oldin butun validatsiya yakunlanishi kerak boʻlsa, `'none'`'dan foydalaning. Validatsiya holatidan qatʼi nazar maʼlumotlarni saqlamoqchi boʻlgan qoralamani saqlash holatlari uchun `'all'`'dan foydalaning.

## `submit()` bilan qoʻlda yuborish {#manual-submission-with-submit}

`FormRoot` direktivi yuborishni ishga tushirishning eng keng tarqalgan usuli, lekin `submit()`'ni toʻgʻridan-toʻgʻri chaqirishingiz ham mumkin. Bu koʻp bosqichli ustalar (wizard), avtomatik saqlash yoki yuborishni forma elementidan tashqaridan ishga tushirish uchun foydali.

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, required, submit} from '@angular/forms/signals';

@Component({
  selector: 'app-contact',
  imports: [FormField],
  template: `
    <label>
      Name
      <input [formField]="contactForm.name" />
    </label>

    <label>
      Email
      <input type="email" [formField]="contactForm.email" />
    </label>

    <button (click)="onSave()">Save</button>
  `,
})
export class Contact {
  contactModel = signal({
    name: '',
    email: '',
  });

  contactForm = form(this.contactModel, (schemaPath) => {
    required(schemaPath.name);
    required(schemaPath.email);
  });

  async onSave() {
    // When calling `submit()` directly, you pass the action as the second argument
    // instead of configuring it in `FormOptions`.
    const success = await submit(this.contactForm, async (field) => {
      const result = await saveContact(field().value());
      if (result.ok) return;

      return {kind: 'serverError', message: 'Failed to save'};
    });

    if (success) {
      // Handle success — navigate, show confirmation, etc.
    }
  }
}
```

## Yon taʼsirlarni qayta ishlash {#handling-side-effects}

`submit()` funksiyasi `Promise<boolean>` qaytaradi — action xatosiz yakunlanganda `true`, validatsiya muvaffaqiyatsiz boʻlganda, action xatolar qaytarganda yoki yuborish allaqachon davom etayotgan boʻlganda `false`. Agar action xato tashlasa, promise rad etiladi. Undan navigatsiya yoki bildirishnomalar kabi yon taʼsirlarni ishga tushirish uchun foydalaning.

```ts
async onSave() {
  const success = await submit(this.contactForm, async (field) => {
    await saveContact(field().value());
  });

  if (success) {
    await this.router.navigate(['/confirmation']);
  }
}
```

Action yon taʼsirga kerak boʻladigan maʼlumotni, masalan, server tomonidan yaratilgan ID'ni ishlab chiqarganda, yon taʼsirni action ichida bajaring:

```ts
async onSave() {
  await submit(this.contactForm, async (field) => {
    const contact = await createContact(field().value());
    await this.router.navigate(['/confirmation', contact.id]);
  });
}
```

`FormRoot`'dan foydalanganda yon taʼsirlar ham `action` ichiga joylashtiriladi, chunki `FormRoot` `submit()`'ni ichki ravishda chaqiradi:

```ts
submission: {
  action: async (field) => {
    const result = await saveContact(field().value());
    if (result.ok) {
      await this.router.navigate(['/confirmation']);
      return;
    }

    return {kind: 'serverError', message: 'Failed to submit form'};
  },
}
```

## Parallel yuborishlar {#concurrent-submissions}

Yuborish davom etayotganda, oʻsha forma yoki uning istalgan avlodi uchun `submit()`'ning keyingi chaqiruvlari action'ni ishga tushirmasdan darhol `false` qaytaradi. Bu foydalanuvchi yuborish amalini tez ketma-ket bir necha marta ishga tushirganda takroriy yuborishlar va yon taʼsirlarning oldini oladi.

## Keyingi qadamlar {#next-steps}

Ushbu qoʻllanma formalarni yuborish va formani yuborish xatolarini qayta ishlashni qamrab oldi. Tegishli qoʻllanmalar Signal Forms'ning boshqa jihatlarini oʻrganadi:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
  <docs-pill href="guide/forms/signals/form-logic" title="Forma logikasini qoʻshish" />
</docs-pill-row>
