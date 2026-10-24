# Validatsiya

Formalar foydalanuvchilar yuborishdan oldin toʻgʻri va toʻliq maʼlumot kiritishini taʼminlash uchun validatsiyaga muhtoj. Validatsiyasiz maʼlumotlar sifati bilan bogʻliq muammolarni serverda hal qilishingiz, noaniq xato xabarlari bilan foydalanuvchiga yomon tajriba taqdim etishingiz va har bir cheklovni qoʻlda tekshirishingiz kerak boʻlardi.

Signal Forms sxemaga asoslangan validatsiya yondashuvini taqdim etadi. Validatsiya qoidalari sxema funksiyasi orqali maydonlarga bogʻlanadi, qiymatlar oʻzgarganda avtomatik ishga tushadi va xatolarni maydon holati signallari orqali ochib beradi. Bu foydalanuvchilar forma bilan ishlashi davomida yangilanib boradigan reaktiv validatsiyani taʼminlaydi.

<docs-code-multifile preview hideCode path="adev/src/content/examples/signal-forms/src/login-validation-complete/app/app.ts">
  <docs-code header="app.ts" path="adev/src/content/examples/signal-forms/src/login-validation-complete/app/app.ts"/>
  <docs-code header="app.html" path="adev/src/content/examples/signal-forms/src/login-validation-complete/app/app.html"/>
  <docs-code header="app.css" path="adev/src/content/examples/signal-forms/src/login-validation-complete/app/app.css"/>
</docs-code-multifile>

## Validatsiya asoslari {#validation-basics}

Signal Forms'da validatsiya `form()`'ga ikkinchi argument sifatida uzatiladigan sxema funksiyasi orqali aniqlanadi.

### Sxema funksiyasi {#the-schema-function}

Sxema funksiyasi validatsiya qoidalaringizni aniqlash imkonini beruvchi `SchemaPathTree` obyektini qabul qiladi:

<docs-code
  header="app.ts"
  path="adev/src/content/examples/signal-forms/src/login-validation-complete/app/app.ts"
  visibleLines="[29,30,31,32,33,34]"
  highlight="[30,31,33]"
/>

Sxema funksiyasi forma ishga tushirilayotganda bir marta bajariladi. Validatsiya qoidalari sxema yoʻli parametri (masalan, `schemaPath.email`, `schemaPath.password`) yordamida maydonlarga bogʻlanadi va maydon qiymatlari oʻzgarganda validatsiya avtomatik ishga tushadi.

NOTE: Sxema callback parametri (ushbu misollarda `schemaPath`) formangizdagi barcha maydonlarga yoʻllarni taqdim etuvchi `SchemaPathTree` obyektidir. Bu parametrni istalgancha nomlashingiz mumkin.

### Validatsiya qanday ishlaydi {#how-validation-works}

Signal Forms'da validatsiya quyidagi namunaga amal qiladi:

1. **Validatsiya qoidalarini sxemada aniqlash** - Sxema funksiyasida validatsiya qoidalarini maydonlarga bogʻlang
2. **Avtomatik bajarilish** - Validatsiya qoidalari maydon qiymatlari oʻzgarganda ishga tushadi
3. **Xatolarning tarqalishi** - Validatsiya xatolari maydon holati signallari orqali ochib beriladi
4. **Reaktiv yangilanishlar** - Validatsiya holati oʻzgarganda UI avtomatik yangilanadi

Interaktiv maydonlar uchun validatsiya har bir qiymat oʻzgarishida ishga tushadi. Yashirin va oʻchirilgan maydonlar validatsiyani bajarmaydi - maydon yana interaktiv boʻlgunga qadar ularning validatsiya qoidalari oʻtkazib yuboriladi.

### Validatsiya vaqti {#validation-timing}

Validatsiya qoidalari quyidagi tartibda bajariladi:

1. **Sinxron validatsiya** - Qiymat oʻzgarganda barcha sinxron validatsiya qoidalari ishga tushadi
2. **Asinxron validatsiya** - Asinxron validatsiya qoidalari faqat barcha sinxron validatsiya qoidalari muvaffaqiyatli oʻtgandan keyin ishga tushadi
3. **Maydon holatini yangilash** - `valid()`, `invalid()`, `errors()` va `pending()` signallari yangilanadi

Sinxron validatsiya qoidalari (`required()`, `email()` kabi) darhol yakunlanadi. Asinxron validatsiya qoidalari (`validateHttp()` kabi) vaqt talab qilishi mumkin va bajarilayotganda `pending()` signalini `true` qiymatiga oʻrnatadi.

Barcha validatsiya qoidalari har bir oʻzgarishda ishga tushadi - validatsiya birinchi xatodan keyin toʻxtab qolmaydi. Agar maydonda `required()` ham, `email()` ham validatsiya qoidasi boʻlsa, ikkalasi ham ishga tushadi va ikkalasi ham bir vaqtning oʻzida xato chiqarishi mumkin.

### Native HTML validatsiyasi {#native-html-validation}

Signal Forms validatsiya qoidalarini bajarish uchun brauzerning oʻrnatilgan [cheklov validatsiyasidan](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Constraint_validation) (constraint validation) **foydalanmaydi**. Bu ataylab shunday qilingan: Signal Forms faqat native forma elementlariga emas, istalgan komponentga forma boshqaruv elementi (control) sifatida ishlash imkonini beradi.

Buning oʻrniga validatsiya qoidalaringiz toʻliq Angular'da bajariladi va validatsiya holati elementning native validlik holati orqali emas, balki `valid()`, `invalid()` va `errors()` kabi maydon holati signallari orqali ochib beriladi. [`FormRoot` direktivi](guide/forms/signals/form-submission) shuningdek, brauzer yuborishni bloklamasligi uchun forma elementiga `novalidate` atributini oʻrnatadi.

Maydon native forma elementiga bogʻlanganda, baʼzi oʻrnatilgan validatsiya qoidalari oʻz cheklovini tegishli native atributga aks ettiradi: `required()`, `min()`, `max()`, `minLength()` va `maxLength()` element qoʻllab-quvvatlasa `required`, `min`, `max`, `minlength` va `maxlength` atributlarini oʻrnatadi. Istisno - `pattern()`: u native `pattern` atributini oʻrnatmaydi. Signal Forms bu atributlarni input xatti-harakatini boshqarish va qulaylikni (accessibility) yaxshilash uchun oʻrnatadi, **native validatsiyani ishga tushirish uchun emas**.

NOTE: Signal Forms native validlik holatini oʻqiydigan bitta holat bor: brauzer native input qiymatini tahlil qila olmasa (masalan, qisman kiritilgan sana), Signal Forms buni tahlil (parse) xatosi sifatida qayd etadi. Shunda ham xato boshqa har qanday validatsiya xatosi kabi maydonning `errors()` signali orqali chiqadi. Tafsilotlar uchun [Qiymatni oʻzgartirish](guide/forms/signals/custom-controls#value-transformation) boʻlimiga qarang.

IMPORTANT: `:valid` va `:invalid` CSS psevdo-klasslari, elementning `validity` xususiyati yoki `validationMessage` kabi native validlik imkoniyatlariga tayanmang. Brauzer aks ettirilgan atributlarning yon taʼsiri sifatida baʼzi input'larni yaroqsiz deb koʻrsatishi mumkin (masalan, qiymati `min`'dan kichik boʻlgan sonli input), lekin bu xatti-harakat validatsiya qoidasi va input turiga qarab farq qiladi va validatsiya holatini kuzatishning qoʻllab-quvvatlanadigan usuli emas.

Boshqaruv elementlariga validatsiya holatiga qarab stil berish uchun klasslarni maydon holati signallariga bogʻlang ([Maydon holatini boshqarish](guide/forms/signals/field-state-management#conditional-error-display) boʻlimiga qarang) yoki avtomatik holat klasslarini sozlang ([Avtomatik holat klasslari](guide/forms/signals/migration#automatic-status-classes) boʻlimiga qarang).

## Oʻrnatilgan validatsiya qoidalari {#built-in-validation-rules}

Signal Forms keng tarqalgan validatsiya holatlari uchun validatsiya qoidalarini taqdim etadi. Barcha oʻrnatilgan validatsiya qoidalari maxsus xato xabarlari va shartli mantiq uchun parametrlar obyektini qabul qiladi.

### required()

`required()` validatsiya qoidasi maydonda qiymat borligini taʼminlaydi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, required} from '@angular/forms/signals';

@Component({
  selector: 'app-registration',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Username
        <input [formField]="registrationForm.username" />
      </label>

      <label>
        Email
        <input type="email" [formField]="registrationForm.email" />
      </label>

      <button type="submit">Register</button>
    </form>
  `,
})
export class RegistrationComponent {
  registrationModel = signal({
    username: '',
    email: '',
  });

  registrationForm = form(this.registrationModel, (schemaPath) => {
    required(schemaPath.username, {message: 'Username is required'});
    required(schemaPath.email, {message: 'Email is required'});
  });
}
```

Maydon qiymati quyidagilardan biri boʻlsa "boʻsh" hisoblanadi, boshqa har qanday qiymatda - shu jumladan `0` va boʻsh massiv `[]` boʻlganda ham - boʻsh emas deb hisoblanadi:

| Shart                    | Misol       |
| ------------------------ | ----------- |
| Qiymat `null`            | `null`      |
| Qiymat `undefined`       | `undefined` |
| Qiymat boʻsh satr        | `''`        |
| Qiymat `false`           | `false`     |
| Qiymat `NaN`             | `NaN`       |

Oxirgi ikkitasini alohida taʼkidlash joiz:

- `false` boʻsh hisoblanadi, chunki bu `<input type="checkbox">`'dagi `required`'ning native semantikasiga mos keladi: belgilanmagan katakcha validatsiyadan oʻtmaydi.
- `NaN` boʻsh hisoblanadi, chunki u odatda tahlil xatosining natijasi boʻlib, yaroqli son emas.

Shartli majburiylik uchun `when` parametridan foydalaning:

```ts
registrationForm = form(this.registrationModel, (schemaPath) => {
  required(schemaPath.promoCode, {
    message: 'Promo code is required for discounts',
    when: ({valueOf}) => valueOf(schemaPath.applyDiscount),
  });
});
```

Validatsiya qoidasi faqat `when` funksiyasi `true` qaytarganda ishga tushadi.

NOTE: `required` boʻsh massivni mavjud (valid) deb hisoblaydi, shuning uchun massiv elementlarining minimal sonini talab qilish uchun [`minLength()`](#minlength-and-maxlength)'dan foydalaning.

### email()

`email()` validatsiya qoidasi email formatining toʻgʻriligini tekshiradi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, email} from '@angular/forms/signals';

@Component({
  selector: 'app-contact',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Your Email
        <input type="email" [formField]="contactForm.email" />
      </label>
    </form>
  `,
})
export class ContactComponent {
  contactModel = signal({email: ''});

  contactForm = form(this.contactModel, (schemaPath) => {
    email(schemaPath.email, {message: 'Please enter a valid email address'});
  });
}
```

`email()` validatsiya qoidasi standart email formati regex'idan foydalanadi. U `user@example.com` kabi manzillarni qabul qiladi, lekin `user@` yoki `@example.com` kabi notoʻgʻri tuzilgan manzillarni rad etadi.

### min() va max() {#min-and-max}

`min()` va `max()` validatsiya qoidalari sonli qiymatlar bilan ishlaydi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, min, max} from '@angular/forms/signals';

@Component({
  selector: 'app-age-form',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Age
        <input type="number" [formField]="ageForm.age" />
      </label>

      <label>
        Rating (1-5)
        <input type="number" [formField]="ageForm.rating" />
      </label>
    </form>
  `,
})
export class AgeFormComponent {
  ageModel = signal({
    age: 0,
    rating: 0,
  });

  ageForm = form(this.ageModel, (schemaPath) => {
    min(schemaPath.age, 18, {message: 'You must be at least 18 years old'});
    max(schemaPath.age, 120, {message: 'Please enter a valid age'});

    min(schemaPath.rating, 1, {message: 'Rating must be at least 1'});
    max(schemaPath.rating, 5, {message: 'Rating cannot exceed 5'});
  });
}
```

Dinamik cheklovlar uchun hisoblangan qiymatlardan foydalanishingiz mumkin:

```ts
ageForm = form(this.ageModel, (schemaPath) => {
  min(schemaPath.participants, () => this.minimumRequired(), {
    message: 'Not enough participants',
  });
});
```

### minDate() va maxDate() {#mindate-and-maxdate}

`minDate()` va `maxDate()` validatsiya qoidalari `Date` qiymatlari bilan, masalan, `<input type="date">`'ga bogʻlangan maydon bilan ishlaydi. Ular shuningdek, oʻsha input'ning `min` va `max` atributlarini ham oʻrnatadi.

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, minDate, maxDate} from '@angular/forms/signals';

@Component({
  selector: 'app-booking-form',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Check-in
        <input type="date" [formField]="bookingForm.checkIn" />
      </label>
    </form>
  `,
})
export class BookingFormComponent {
  bookingModel = signal<{checkIn: Date | null}>({checkIn: null});

  bookingForm = form(this.bookingModel, (schemaPath) => {
    minDate(schemaPath.checkIn, new Date('2026-06-01'), {message: 'Bookings open on June 1'});
    maxDate(schemaPath.checkIn, new Date('2026-08-31'), {message: 'Bookings close on August 31'});
  });
}
```

IMPORTANT: `<input type="date">` foydalanuvchining vaqt mintaqasidan qatʼi nazar `Date` qiymatlarini UTC boʻyicha yarim tun vaqtida oʻqiydi va yozadi, chunki brauzerning `valueAsDate` xususiyati shunday ishlaydi. Chegaralarni ham shu tarzda yarating, masalan, `new Date('2026-06-01')` yoki `new Date(Date.UTC(2026, 5, 1))` bilan. Mahalliy vaqtdan yaratilgan `Date`, masalan, `new Date(2026, 5, 1)` yoki `new Date()`, foydalanuvchining UTC siljishi miqdoriga suriladi. Vaqt mintaqasiga qarab `min` yoki `max` atributi bir kunga farq qilishi va chegara sanasining oʻzi rad etilishi mumkin.

Bugundan oldin boʻlmagan sanani talab qilish uchun foydalanuvchi vaqt mintaqasidagi bugungi kalendar sanasini UTC boʻyicha yarim tun koʻrinishida ifodalab ishlating:

```ts
const now = new Date();
const today = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));

minDate(schemaPath.checkIn, today, {message: 'Check-in cannot be in the past'});
```

`new Date()`'ni toʻgʻridan-toʻgʻri uzatish bugungi sanani rad etishi mumkin, chunki input'da tanlangan qiymat UTC boʻyicha yarim tun boʻlib, joriy vaqtdan oldinroq. Bu UTC'da va undan orqada boʻlgan vaqt mintaqalarida yuz beradi.

### minLength() va maxLength() {#minlength-and-maxlength}

`minLength()` va `maxLength()` validatsiya qoidalari satrlar va massivlar bilan ishlaydi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, minLength, maxLength} from '@angular/forms/signals';

@Component({
  selector: 'app-password-form',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Password
        <input type="password" [formField]="passwordForm.password" />
      </label>

      <label>
        Bio
        <textarea [formField]="passwordForm.bio"></textarea>
      </label>
    </form>
  `,
})
export class PasswordFormComponent {
  passwordModel = signal({
    password: '',
    bio: '',
  });

  passwordForm = form(this.passwordModel, (schemaPath) => {
    minLength(schemaPath.password, 8, {message: 'Password must be at least 8 characters'});
    maxLength(schemaPath.password, 100, {message: 'Password is too long'});

    maxLength(schemaPath.bio, 500, {message: 'Bio cannot exceed 500 characters'});
  });
}
```

Satrlar uchun "uzunlik" belgilar sonini anglatadi. Massivlar uchun "uzunlik" elementlar sonini anglatadi.

### pattern()

`pattern()` validatsiya qoidasi qiymatni regulyar ifoda boʻyicha tekshiradi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, pattern} from '@angular/forms/signals';

@Component({
  selector: 'app-phone-form',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Phone Number
        <input [formField]="phoneForm.phone" placeholder="555-123-4567" />
      </label>

      <label>
        Postal Code
        <input [formField]="phoneForm.postalCode" placeholder="12345" />
      </label>
    </form>
  `,
})
export class PhoneFormComponent {
  phoneModel = signal({
    phone: '',
    postalCode: '',
  });

  phoneForm = form(this.phoneModel, (schemaPath) => {
    pattern(schemaPath.phone, /^\d{3}-\d{3}-\d{4}$/, {
      message: 'Phone must be in format: 555-123-4567',
    });

    pattern(schemaPath.postalCode, /^\d{5}$/, {
      message: 'Postal code must be 5 digits',
    });
  });
}
```

Keng tarqalgan namunalar:

| Namuna turi           | Regulyar ifoda          | Misol        |
| --------------------- | ----------------------- | ------------ |
| Telefon               | `/^\d{3}-\d{3}-\d{4}$/` | 555-123-4567 |
| Pochta indeksi (AQSH) | `/^\d{5}$/`             | 12345        |
| Harf-raqamli          | `/^[a-zA-Z0-9]+$/`      | abc123       |
| URL uchun xavfsiz     | `/^[a-zA-Z0-9_-]+$/`    | my-url_123   |

## Massiv elementlarini validatsiya qilish {#validation-of-array-items}

Formalar ichki obyektlar massivlarini (masalan, buyurtma elementlari roʻyxatini) oʻz ichiga olishi mumkin. Massivdagi har bir elementga validatsiya qoidalarini qoʻllash uchun sxema funksiyangiz ichida `applyEach()`'dan foydalaning. `applyEach()` massiv yoʻli boʻylab yuradi va har bir element uchun yoʻl taqdim etadi; unda validatorlarni yuqori darajadagi maydonlardagi kabi qoʻllashingiz mumkin.

```ts
import {Component, signal} from '@angular/core';
import {applyEach, FormField, form, min, required, SchemaPathTree} from '@angular/forms/signals';

type Item = {name: string; quantity: number};

interface Order {
  title: string;
  description: string;
  items: Item[];
}

function ItemSchema(item: SchemaPathTree<Item>) {
  required(item.name, {message: 'Item name is required'});
  min(item.quantity, 1, {message: 'Quantity must be at least 1'});
}

@Component(/* ... */)
export class OrderComponent {
  orderModel = signal<Order>({
    title: '',
    description: '',
    items: [{name: '', quantity: 0}],
  });

  orderForm = form(this.orderModel, (schemaPath) => {
    required(schemaPath.title);
    required(schemaPath.description);

    applyEach(schemaPath.items, ItemSchema);
  });
}
```

## Validatsiya xatolari {#validation-errors}

Validatsiya qoidalari bajarilmaganda ular nima notoʻgʻri ketganini tavsiflovchi xato obyektlarini hosil qiladi. Xato tuzilmasini tushunish foydalanuvchilarga aniq fikr-mulohaza berishga yordam beradi.

NOTE: Bu boʻlim validatsiya qoidalari hosil qiladigan xatolarni yoritadi. Validatsiya xatolarini UI'da koʻrsatish va ishlatish uchun [Maydon holatini boshqarish qoʻllanmasiga](guide/forms/signals/field-state-management) qarang.

### Xato tuzilmasi {#error-structure}

Har bir validatsiya xatosi obyekti quyidagi xususiyatlarni oʻz ichiga oladi:

| Xususiyat | Tavsif                                                                       |
| --------- | ---------------------------------------------------------------------------- |
| `kind`    | Bajarilmagan validatsiya qoidasi (masalan, "required", "email", "minLength") |
| `message` | Ixtiyoriy, odam oʻqishi uchun moʻljallangan xato xabari                      |

Oʻrnatilgan validatsiya qoidalari `kind` xususiyatini avtomatik oʻrnatadi. `message` xususiyati ixtiyoriy - validatsiya qoidasi parametrlari orqali maxsus xabarlar berishingiz mumkin.

### Maxsus xato xabarlari {#custom-error-messages}

Barcha oʻrnatilgan validatsiya qoidalari maxsus xato matni uchun `message` parametrini qabul qiladi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, required, minLength} from '@angular/forms/signals';

@Component({
  selector: 'app-signup',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Username
        <input [formField]="signupForm.username" />
      </label>

      <label>
        Password
        <input type="password" [formField]="signupForm.password" />
      </label>
    </form>
  `,
})
export class SignupComponent {
  signupModel = signal({
    username: '',
    password: '',
  });

  signupForm = form(this.signupModel, (schemaPath) => {
    required(schemaPath.username, {
      message: 'Please choose a username',
    });

    required(schemaPath.password, {
      message: 'Password cannot be empty',
    });
    minLength(schemaPath.password, 12, {
      message: 'Password must be at least 12 characters for security',
    });
  });
}
```

Maxsus xabarlar aniq, konkret boʻlishi va foydalanuvchilarga muammoni qanday hal qilishni aytishi kerak. "Invalid input" oʻrniga "Password must be at least 12 characters for security" kabi xabardan foydalaning.

### Bir maydonda bir nechta xato {#multiple-errors-per-field}

Maydonda bir nechta validatsiya qoidasi boʻlsa, har bir validatsiya qoidasi mustaqil ishga tushadi va xato chiqarishi mumkin:

```ts
signupForm = form(this.signupModel, (schemaPath) => {
  required(schemaPath.email, {message: 'Email is required'});
  email(schemaPath.email, {message: 'Enter a valid email address'});
  minLength(schemaPath.email, 5, {message: 'Email is too short'});
});
```

Agar email maydoni boʻsh boʻlsa, faqat `required()` xatosi koʻrinadi. Agar foydalanuvchi "a@b" deb yozsa, `email()` ham, `minLength()` ham xato chiqaradi. Barcha validatsiya qoidalari ishga tushadi - validatsiya birinchi muvaffaqiyatsizlikdan keyin toʻxtamaydi.

TIP: Foydalanuvchi maydon bilan ishlashidan oldin xatolar koʻrinishining oldini olish uchun shablonlaringizda `touched() && invalid()` namunasidan foydalaning. Validatsiya xatolarini koʻrsatish boʻyicha toʻliq qoʻllanma uchun [Maydon holatini boshqarish qoʻllanmasiga](guide/forms/signals/field-state-management#conditional-error-display) qarang.

## Maxsus validatsiya qoidalari {#custom-validation-rules}

Oʻrnatilgan validatsiya qoidalari keng tarqalgan holatlarni qamrab olsa-da, biznes qoidalari, murakkab formatlar yoki sohaga xos cheklovlar uchun koʻpincha maxsus validatsiya mantigʻi kerak boʻladi.

### validate()'dan foydalanish {#using-validate}

`validate()` funksiyasi maxsus validatsiya qoidalarini yaratadi. U maydon kontekstiga murojaat qiluvchi va quyidagilarni qaytaruvchi validator funksiyasini qabul qiladi:

| Qaytariladigan qiymat   | Maʼnosi         |
| ----------------------- | --------------- |
| Xato obyekti            | Qiymat yaroqsiz |
| `null` yoki `undefined` | Qiymat yaroqli  |

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, validate} from '@angular/forms/signals';

@Component({
  selector: 'app-url-form',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Website URL
        <input [formField]="urlForm.website" />
      </label>
    </form>
  `,
})
export class UrlFormComponent {
  urlModel = signal({website: ''});

  urlForm = form(this.urlModel, (schemaPath) => {
    validate(schemaPath.website, ({value}) => {
      if (!value().startsWith('https://')) {
        return {
          kind: 'https',
          message: 'URL must start with https://',
        };
      }

      return null;
    });
  });
}
```

Validator funksiyasi quyidagilarga ega `FieldContext` obyektini qabul qiladi:

| Xususiyat       | Turi       | Tavsif                                                    |
| --------------- | ---------- | --------------------------------------------------------- |
| `value`         | Signal     | Maydonning joriy qiymatini saqlovchi signal               |
| `state`         | FieldState | Maydon holatiga havola                                    |
| `fieldTree`     | FieldTree  | Maydonlar daraxtiga havola                                |
| `valueOf()`     | Metod      | Boshqa maydon qiymatini yoʻl boʻyicha olish               |
| `stateOf()`     | Metod      | Boshqa maydon holatini yoʻl boʻyicha olish                |
| `fieldTreeOf()` | Metod      | Boshqa maydonning maydonlar daraxtini yoʻl boʻyicha olish |
| `pathKeys`      | Signal     | Ildizdan joriy maydongacha boʻlgan yoʻl kalitlari         |

NOTE: Ichki maydonlar shuningdek `key` signaliga, massiv elementi maydonlari esa `key` va `index` signallarining ikkalasiga ega.

Validatsiya muvaffaqiyatsiz boʻlganda `kind` va `message`'ga ega xato obyektini qaytaring. Validatsiya oʻtganda `null` yoki `undefined` qaytaring.

### validateTree()'dan foydalanish {#using-validatetree}

`validateTree()` funksiyasi bir nechta maydonga yoʻnaltirilishi yoki butun bir ichki daraxt (subtree) uchun murakkab validatsiya mantigʻini taqdim etishi mumkin boʻlgan maxsus validatsiya qoidalarini yaratadi.

```angular-ts
import {Component, model} from '@angular/core';
import {form, FormField, validateTree} from '@angular/forms/signals';

interface User {
  firstName: string;
  lastName: string;
}

@Component({/* ... */})
export class UserFormComponent {
  readonly userModel = model<User>({
    firstName: '',
    lastName: '',
  });

  userForm = form(this.userModel, (path) => {
    validateTree(path, (ctx) => {
      if (ctx.valueOf(path.firstName).length < 5) {
        return {
          kind: 'minLength5',
          message: 'First name must be at least 5 characters',
          fieldTree: ctx.fieldTree.lastName,
        };
      }

      return null;
    });
  });
}
```

`validateTree()` validator funksiyasi `validate()` bilan bir xil `FieldContext` obyektini qabul qiladi.

### Qayta ishlatiladigan validatsiya qoidalari {#reusable-validation-rules}

`validate()`'ni oʻrab, qayta ishlatiladigan validatsiya qoidasi funksiyalarini yarating:

```ts
function url(path: SchemaPath<string>, options?: {message?: string}) {
  validate(path, ({value}) => {
    try {
      new URL(value());
      return null;
    } catch {
      return {
        kind: 'url',
        message: options?.message || 'Enter a valid URL',
      };
    }
  });
}

function phoneNumber(path: SchemaPath<string>, options?: {message?: string}) {
  validate(path, ({value}) => {
    const phoneRegex = /^\d{3}-\d{3}-\d{4}$/;

    if (!phoneRegex.test(value())) {
      return {
        kind: 'phoneNumber',
        message: options?.message || 'Phone must be in format: 555-123-4567',
      };
    }

    return null;
  });
}
```

Maxsus validatsiya qoidalarini oʻrnatilgan validatsiya qoidalari kabi ishlatishingiz mumkin:

```ts
urlForm = form(this.urlModel, (schemaPath) => {
  url(schemaPath.website, {message: 'Please enter a valid website URL'});
  phoneNumber(schemaPath.phone);
});
```

## Maydonlararo validatsiya {#cross-field-validation}

Maydonlararo validatsiya bir nechta maydon qiymatlarini oʻzaro taqqoslaydi yoki bogʻlaydi.

Maydonlararo validatsiyaning keng tarqalgan holati - parolni tasdiqlash:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, required, minLength, validate} from '@angular/forms/signals';

@Component({
  selector: 'app-password-change',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        New Password
        <input type="password" [formField]="passwordForm.password" />
      </label>

      <label>
        Confirm Password
        <input type="password" [formField]="passwordForm.confirmPassword" />
      </label>

      <button type="submit">Change Password</button>
    </form>
  `,
})
export class PasswordChangeComponent {
  passwordModel = signal({
    password: '',
    confirmPassword: '',
  });

  passwordForm = form(this.passwordModel, (schemaPath) => {
    required(schemaPath.password, {message: 'Password is required'});
    minLength(schemaPath.password, 8, {message: 'Password must be at least 8 characters'});

    required(schemaPath.confirmPassword, {message: 'Please confirm your password'});

    validate(schemaPath.confirmPassword, ({value, valueOf}) => {
      const confirmPassword = value();
      const password = valueOf(schemaPath.password);

      if (confirmPassword !== password) {
        return {
          kind: 'passwordMismatch',
          message: 'Passwords do not match',
        };
      }

      return null;
    });
  });
}
```

Tasdiqlash validatsiya qoidasi `valueOf(schemaPath.password)` yordamida parol maydoni qiymatiga murojaat qiladi va uni tasdiqlash qiymati bilan taqqoslaydi. Bu validatsiya qoidasi reaktiv ishlaydi - parollardan istalgan biri oʻzgarsa, validatsiya avtomatik qayta bajariladi.

## Shartli validatsiya {#conditional-validation}

Baʼzan validatsiya qoidasi faqat maʼlum shartlarda qoʻllanishi kerak, masalan, yetkazib berish manzilini faqat buyurtma xalqaro yuborilganda tekshirish yoki union tipli maydonning har bir variantiga alohida qoidalar toʻplamini qoʻllash.

Validatsiya qoidalari sxema funksiyasida joylashgani uchun ularni sxemalarni tuzishda ishlatiladigan oʻsha strukturaviy funksiyalar yordamida shartli qoʻllaysiz:

- Boshqa maydonlarning qiymatlari ham kiruvchi reaktiv forma holatiga asoslanib qoidalar guruhini faollashtirish uchun [`applyWhen()`](guide/forms/signals/form-logic#conditional-logic-with-applywhen)'dan foydalaning.
- Maydonning oʻz qiymatiga asoslanib qoidalarni qoʻllash uchun [`applyWhenValue()`](guide/forms/signals/schemas#type-narrowing-with-applywhenvalue)'dan foydalaning. Predikat tip himoyachisi (type guard) boʻlsa, qoidalar toraytirilgan qiymat tipiga ega boʻladi, bu esa uni diskriminatsiyalangan union'lar va boshqa variantli tiplarni tekshirishning tavsiya etilgan usuliga aylantiradi.

Qayta ishlatiladigan sxemalar va diskriminatsiyalangan union'larni ham oʻz ichiga olgan toʻliq misollar uchun [Sxemalar va sxema kompozitsiyasi qoʻllanmasiga](guide/forms/signals/schemas) qarang.

## Asinxron validatsiya {#async-validation}

Asinxron validatsiya tashqi maʼlumot manbalarini talab qiluvchi validatsiyani, masalan, serverda foydalanuvchi nomi bandligini tekshirish yoki API orqali tekshirishni amalga oshiradi.

### validateHttp()'dan foydalanish {#using-validatehttp}

`validateHttp()` funksiyasi HTTP'ga asoslangan validatsiyani bajaradi:

```angular-ts
import {Component, signal} from '@angular/core';
import {form, FormField, required, validateHttp} from '@angular/forms/signals';

@Component({
  selector: 'app-username-form',
  imports: [FormField],
  template: `
    <form novalidate>
      <label>
        Username
        <input [formField]="usernameForm.username" />

        @if (usernameForm.username().pending()) {
          <span class="checking">Checking availability...</span>
        }
      </label>
    </form>
  `,
})
export class UsernameFormComponent {
  usernameModel = signal({username: ''});

  usernameForm = form(this.usernameModel, (schemaPath) => {
    required(schemaPath.username, {message: 'Username is required'});

    validateHttp(schemaPath.username, {
      request: ({value}) => `/api/check-username?username=${value()}`,
      onSuccess: (response: any) => {
        if (response.taken) {
          return {
            kind: 'usernameTaken',
            message: 'Username is already taken',
          };
        }
        return null;
      },
      onError: (error) => ({
        kind: 'networkError',
        message: 'Could not verify username availability',
      }),
    });
  });
}
```

`validateHttp()` validatsiya qoidasi:

1. `request` funksiyasi qaytargan URL yoki soʻrovni chaqiradi
2. `onSuccess` yordamida muvaffaqiyatli javobni validatsiya xatosiga yoki `null`'ga aylantiradi
3. `onError` yordamida soʻrov muvaffaqiyatsizliklarini (tarmoq xatolari, HTTP xatolari) qayta ishlaydi
4. Soʻrov bajarilayotganda `pending()`'ni `true` qiymatiga oʻrnatadi
5. Faqat barcha sinxron validatsiya qoidalari muvaffaqiyatli oʻtgandan keyin ishga tushadi

### Kutish holati {#pending-state}

Asinxron validatsiya bajarilayotganda maydonning `pending()` signali `true` qaytaradi. Yuklanish indikatorlarini koʻrsatish uchun shundan foydalaning:

```angular-html
@if (form.username().pending()) {
  <span class="spinner">Checking...</span>
}
```

`valid()` signali validatsiya kutish holatida boʻlganda, hali xatolar boʻlmasa ham, `false` qaytaradi. `invalid()` signali faqat xatolar mavjud boʻlganda `true` qaytaradi.

## Sxema validatsiya kutubxonalari bilan integratsiya {#integration-with-schema-validation-libraries}

Signal Forms [Standard Schema](https://standardschema.dev/)'ga mos keluvchi [Zod](https://zod.dev/) yoki [Valibot](https://valibot.dev/) kabi kutubxonalarni oʻrnatilgan holda qoʻllab-quvvatlaydi. Integratsiya `validateStandardSchema` funksiyasi orqali taqdim etiladi. Bu Signal Forms'ning reaktiv validatsiya afzalliklarini saqlab qolgan holda mavjud sxemalardan foydalanish imkonini beradi.

```ts
import {form, validateStandardSchema} from '@angular/forms/signals';
import * as z from 'zod';

// Define your schema
const userSchema = z.object({
  email: z.email(),
  password: z.string().min(8),
});

// Use with Signal Forms
const userForm = form(signal({email: '', password: ''}), (schemaPath) => {
  validateStandardSchema(schemaPath, userSchema);
});
```

### Dinamik sxemalar {#dynamic-schemas}

Statik sxema oʻrniga signal uzatishingiz mumkin, shunda validatsiya sxemasi oʻz bogʻliqliklari oʻzgarganda avtomatik yangilanadi.

```angular-ts
import {Component, computed, signal} from '@angular/core';
import {form, FormField, validateStandardSchema} from '@angular/forms/signals';
import z from 'zod';

@Component({/* ... */})
export class DynamicSchema {
  model = signal({document: '', type: 'dni'});

  // Schema reacts automatically to type changes
  schema = computed(() =>
    z.object({
      document:
        this.model().type === 'dni'
          ? z.string().length(8, 'DNI must be 8 digits')
          : z.string().min(12, 'Passport must be at least 12 characters'),
    }),
  );

  f = form(this.model, (p) => validateStandardSchema(p, () => this.schema()));
}
```

## Keyingi qadamlar {#next-steps}

Ushbu qoʻllanma validatsiya qoidalarini yaratish va qoʻllashni yoritdi. Tegishli qoʻllanmalar Signal Forms'ning boshqa jihatlarini oʻrganadi:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
  <docs-pill href="guide/forms/signals/models" title="Forma modellari" />
  <docs-pill href="guide/forms/signals/form-logic" title="Forma mantigʻini qoʻshish" />
  <docs-pill href="guide/forms/signals/schemas" title="Sxemalar va sxema kompozitsiyasi" />
</docs-pill-row>
