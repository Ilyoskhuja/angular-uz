# Maydonlararo mantiq

**Maydonlararo mantiq** (cross-field logic) bir maydonning istalgan qoidasi, validatsiyasi yoki xatti-harakati boshqa maydonning qiymati yoki holatiga bogʻliq boʻlganda zarur boʻladi.

Signal forms har bir qoida funksiyasiga **maydon konteksti** (field context) taqdim etadi. Maydon konteksti joriy maydonning qiymati va holatiga murojaat qilish imkonini beradi, shuningdek `valueOf()`, `stateOf()` va `fieldTreeOf()` yordamida formadagi boshqa maydonlarni oʻqish imkonini beradi.

Bu qoʻllanma maydon konteksti API'sini chuqur yoritadi va keng tarqalgan maydonlararo namunalarni koʻrsatadi. Bitta maydonni validatsiya qilish haqida [Validatsiya boʻyicha qoʻllanma](/guide/forms/signals/validation) bilan tanishing.

## Maydon kontekstini tushunish {#understanding-the-field-context}

Signal forms'dagi har bir qoida funksiyasi **maydon konteksti** parametrini qabul qiladi — bu joriy maydonni tavsiflovchi va formaning qolgan qismiga murojaat qilish imkonini beruvchi obyekt.

Joriy maydon uchun murojaat qilishingiz mumkin boʻlgan uchta xususiyat mavjud:

| Xususiyat   | Turi                 | Tavsif                                                                     |
| ----------- | -------------------- | -------------------------------------------------------------------------- |
| `value`     | `Signal<TValue>`     | Joriy maydonning qiymati signal sifatida                                   |
| `state`     | `FieldState<TValue>` | Joriy maydonning holati (validlik, xatolar, touched, dirty kabi)           |
| `fieldTree` | `FieldTree<TValue>`  | Joriy maydonning daraxti, ichki maydonlarga dasturiy murojaat qilish uchun |

Maydonlararo mantiq uchun quyidagi uchta xususiyat formaning boshqa qismlariga murojaat qilish imkonini beradi:

| Xususiyat       | Turi                           | Tavsif                                                                                                                                                       |
| --------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `valueOf()`     | `(path) => PValue`             | Eng keng tarqalgani. Taqqoslash yoki hisoblash uchun boshqa maydonning xom qiymati kerak boʻlganda foydalaning.                                             |
| `stateOf()`     | `(path) => FieldState<PValue>` | Mantigʻingiz boshqa maydonning holatiga, masalan, uning valid, touched yoki dirty ekanligiga bogʻliq boʻlganda foydalaning.                                 |
| `fieldTreeOf()` | `(path) => FieldTree<PModel>`  | Boshqa maydonning daraxtiga dasturiy murojaat kerak boʻlganda, masalan, validateTree bilan muayyan ichki maydonga xatolarni yoʻnaltirishda foydalaning.     |

Joriy maydon (tugash sanasi) formadagi boshlanish sanasidan keyin kelishini tekshirish uchun `value` va `valueOf()`'dan foydalanish misoli:

```ts
import {Component, signal} from '@angular/core';
import {form, validate} from '@angular/forms/signals';

@Component({/* ... */})
export class EventForm {
  eventModel = signal({
    startDate: new Date('2026-06-01'),
    endDate: new Date('2026-06-05'),
  });

  eventForm = form(this.eventModel, (schemaPath) => {
    validate(schemaPath.endDate, ({value, valueOf}) => {
      if (value() <= valueOf(schemaPath.startDate)) {
        return {
          kind: 'invalidDateRange',
          message: 'End date must be after start date',
        };
      }

      return null;
    });
  });
}
```

NOTE: `fieldContext` parametri odatda qoidaga kerak boʻlgan narsalarnigina ajratib olish uchun destrukturizatsiya qilinadi. Bu qoʻllanmadagi qolgan misollar shu namunadan foydalanadi.

## Maydonlararo validatsiya namunalari {#cross-field-validation-patterns}

Oldingi boʻlimdagi sana diapazoni misoli tugash sanasini boshlanish sanasiga nisbatan tekshiradi. Qoida `valueOf(schemaPath.startDate)`'ni oʻqigani uchun, u ikkala sanadan istalgani oʻzgarganda avtomatik qayta hisoblanadi. Boshqacha aytganda, xato holatini toʻgʻri saqlash uchun bitta validator kifoya.

Biroq bu yagona validator xatoni faqat tugash sanasi maydoniga qoʻyadi. Diapazon notoʻgʻri boʻlganda ikkala maydon ham xato koʻrsatishini istasangiz, har bir maydonga mos validatsiya qoidasini qoʻshing:

```ts
import {Component, signal} from '@angular/core';
import {form, validate} from '@angular/forms/signals';

@Component({/* ... */})
export class EventForm {
  eventModel = signal({
    startDate: new Date('2026-06-01'),
    endDate: new Date('2026-06-05'),
  });

  eventForm = form(this.eventModel, (schemaPath) => {
    validate(schemaPath.startDate, ({value, valueOf}) => {
      if (value() >= valueOf(schemaPath.endDate)) {
        return {
          kind: 'invalidDateRange',
          message: 'Start date must be before end date',
        };
      }
      return null;
    });

    validate(schemaPath.endDate, ({value, valueOf}) => {
      if (value() <= valueOf(schemaPath.startDate)) {
        return {
          kind: 'invalidDateRange',
          message: 'End date must be after start date',
        };
      }
      return null;
    });
  });
}
```

Ikkala qoida ham boshqa maydonni oʻqish uchun `valueOf()`'dan foydalanadi. Har bir qoida reaktiv boʻlgani uchun, istalgan sananing oʻzgarishi ikkala validatsiyani avtomatik qayta hisoblaydi.

NOTE: Qoida bir nechta maydonni qamrab olganda, xato qayerga tegishli boʻlishini hal qilishingiz kerak: muayyan maydonga, bir nechta maydonga yoki ota maydonga. Umuman olganda, xatoni foydalanuvchi muammoni tuzatish uchun eng ehtimol murojaat qiladigan joyga qoʻying.

### Shartli talablar {#conditional-requirements}

Baʼzi formalarda ayrim maydonlar faqat maʼlum shartlarda majburiy boʻladi. Masalan, roʻyxatdan oʻtish formasi kompaniya nomini faqat foydalanuvchi biznes hisob turini tanlaganda talab qilishi mumkin:

```ts
import {Component, signal} from '@angular/core';
import {form, required} from '@angular/forms/signals';

@Component({/* ... */})
export class RegistrationForm {
  registrationModel = signal({
    accountType: 'personal' as 'personal' | 'business',
    companyName: '',
  });

  registrationForm = form(this.registrationModel, (schemaPath) => {
    required(schemaPath.companyName, {
      when: ({valueOf}) => valueOf(schemaPath.accountType) === 'business',
      message: 'Company name is required for business accounts',
    });
  });
}
```

`when` opsiyasi istalgan boshqa qoida funksiyasi bilan bir xil maydon kontekstini qabul qiladi, shuning uchun `valueOf` bir xil ishlaydi. Foydalanuvchi `'personal'`ga qaytganda shart qayta hisoblanadi va talab — oʻz xatosi bilan birga — avtomatik bekor boʻladi.

Qoʻlda `validate()` tekshiruvi oʻrniga `required()`'ni `when` bilan ishlatish maydonga toʻgʻri required metamaʼlumotlarini ham qoʻshadi, bu esa ekran oʻquvchilari (screen reader) uchun maydonni majburiy deb belgilash kabi foydalanish qulayligi (accessibility) imkoniyatlarini yoqadi.

### Boshqa maydonning holatiga asoslangan validatsiya {#validating-based-on-another-fields-state}

Hozirgacha misollar boshqa maydonning qiymatini oʻqish uchun `valueOf()`'dan foydalandi. Baʼzan mantigʻingiz boshqa maydonning qiymatiga emas, _holatiga_ bogʻliq boʻladi — u valid, touched yoki dirty ekanligiga. Buning uchun `stateOf()`'dan foydalaning.

Masalan, parolni tasdiqlash maydoni moslikni faqat foydalanuvchi parol maydoni bilan oʻzaro aloqa qilganidan soʻng tekshirishi kerak. Foydalanuvchi parolga hali tegmagan boʻlsa, tasdiqlashda nomuvofiqlikni belgilash erta hisoblanadi:

```ts
import {Component, signal} from '@angular/core';
import {form, validate} from '@angular/forms/signals';

@Component({/* ... */})
export class PasswordForm {
  passwordModel = signal({
    password: '',
    confirmPassword: '',
  });

  passwordForm = form(this.passwordModel, (schemaPath) => {
    validate(schemaPath.confirmPassword, ({value, valueOf, stateOf}) => {
      if (!stateOf(schemaPath.password).touched()) {
        return null;
      }
      if (value() !== valueOf(schemaPath.password)) {
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

`stateOf()` chaqiruvi boshqa maydonning [maydon holatini](api/forms/signals/FieldState) qaytaradi va sizga `invalid()`, `touched()` va `dirty()` kabi signallarga murojaat qilish imkonini beradi. Bular signal boʻlgani uchun, parol maydonining validligi oʻzgarganda qoida qayta hisoblanadi.

CRITICAL: Maydoningiz validatsiyasiga bogʻliq boʻlgan holatni oʻqimaslikka ehtiyot boʻling, chunki bu yopiq sikl hosil qiladi. Masalan, ota maydon valid ekanligini tekshiruvchi validator cheksiz siklga olib keladi, chunki ota maydonning validligi uning ichki maydonlarining validligiga (shu jumladan sizning validatoringizga) bogʻliq.

## validateTree'dan foydalanish {#using-validatetree}

Hozirgacha misollar alohida maydonlarni tekshirish uchun `validate()`'dan foydalandi. Baʼzan mantiq tabiatan guruhdagi bir nechta maydonga tegishli boʻlgan maydonlar guruhini validatsiya qilish va xatolarni uning ichidagi muayyan ichki maydonlarga yoʻnaltirish kerak boʻladi. `validateTree` ana shunday holatlar uchun juda mos.

Masalan, Sudoku boshqotirmasida har bir qator takrorlanmas sonlardan iborat boʻlishi kerak. Bu guruh darajasidagi qoida: butun qatorni tekshirasiz, soʻngra uni buzgan muayyan kataklarni belgilaysiz. Bunday validatsiyani alohida maydonlarda `validate` bilan toza ifodalab boʻlmaydi, chunki har bir katak boshqa barcha kataklar haqida bilishi kerak boʻlardi.

```ts
import {Component, signal} from '@angular/core';
import {form, validateTree} from '@angular/forms/signals';

@Component({/* ... */})
export class SudokuRow {
  rowModel = signal({
    cell1: 1,
    cell2: 3,
    cell3: 1,
    cell4: 4,
  });

  rowForm = form(this.rowModel, (schemaPath) => {
    validateTree(schemaPath, ({value, fieldTreeOf}) => {
      const row = value();
      const entries = [
        {val: row.cell1, fieldTree: fieldTreeOf(schemaPath.cell1)},
        {val: row.cell2, fieldTree: fieldTreeOf(schemaPath.cell2)},
        {val: row.cell3, fieldTree: fieldTreeOf(schemaPath.cell3)},
        {val: row.cell4, fieldTree: fieldTreeOf(schemaPath.cell4)},
      ];

      const counts = new Map<number, number>();
      for (const {val} of entries) {
        if (val !== 0) {
          counts.set(val, (counts.get(val) ?? 0) + 1);
        }
      }

      const errors = entries
        .filter(({val}) => val !== 0 && (counts.get(val) ?? 0) > 1)
        .map(({val, fieldTree}) => ({
          kind: 'duplicateInRow',
          message: `${val} already appears in this row`,
          fieldTree,
        }));

      return errors.length > 0 ? errors : null;
    });
  });
}
```

Validator ota maydonda (qatorda) ishlaydi, barcha katak qiymatlarini oʻqiydi, takrorlanishlarni sanaydi va takrorlangan son boʻlgan har bir katak uchun xato qaytaradi. Har bir xatodagi `fieldTree` xususiyati Angular'ga xatoni aynan qaysi katak koʻrsatishi kerakligini bildiradi. `fieldTree`siz xatolar qatorning oʻziga tegishli boʻlardi — foydalanuvchi ularni koʻrishi kerak boʻlgan joyga emas.

`validateTree` xatolar massivini qaytara olgani uchun, bitta validator bir vaqtning oʻzida bir nechta katakni belgilashi mumkin. Har bir xato oʻz maqsadiga ishora qiluvchi `fieldTree`ni oʻz ichiga oladi, shuning uchun Angular xatolarni toʻgʻri maydonlarga yoʻnaltiradi.

### validateTree va validate'dan qachon foydalanish {#when-to-use-validatetree-vs-validate}

Xato tekshirilayotgan maydonga tegishli boʻlganda — qoida boshqa maydonlardan oʻqisa ham — `validate()`'ni `valueOf()` bilan afzal koʻring. `validateTree`'ga quyidagi hollarda murojaat qiling:

- Validatsiya mantigʻi tabiatan biror bitta maydonga emas, maydonlar guruhiga tegishli boʻlsa
- Validator turli ichki maydonlarga qaratilgan xatolarni qaytarishi kerak boʻlsa

TIP: `validateTree` va uning qaytarish turi bilan tanishish uchun [Validatsiya boʻyicha qoʻllanma](/guide/forms/signals/validation) bilan tanishing.

## Keyingi qadamlar {#next-steps}

Bu qoʻllanma maydon konteksti API'si va keng tarqalgan maydonlararo namunalarni yoritdi. Signal Forms'ning tegishli qoʻllanmalari haqida koʻproq bilish uchun quyidagilarni koʻrib chiqing:

<docs-pill-row>
  <docs-pill href="guide/forms/signals/validation" title="Validatsiya" />
  <docs-pill href="guide/forms/signals/field-state-management" title="Maydon holatini boshqarish" />
  <docs-pill href="guide/forms/signals/custom-controls" title="Maxsus boshqaruv elementlari" />
</docs-pill-row>
