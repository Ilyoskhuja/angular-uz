# `ng-content` bilan ota komponentdan shablonlarni render qilish

`<ng-content>` — belgilash (markup) yoki shablon fragmentini qabul qiladigan va komponentlar kontentni qanday render qilishini boshqaradigan maxsus element. U haqiqiy DOM elementini render qilmaydi.

Quyida oʻz ota komponentidan istalgan belgilashni qabul qiladigan `BaseButton` komponentining misoli keltirilgan.

```angular-ts {header:'base-button/base-button.ts'}
import {Component} from '@angular/core';

@Component({
  selector: 'button[baseButton]',
  template: `<ng-content />`,
})
export class BaseButton {}
```

```angular-ts {header:'app.ts'}
import {Component} from '@angular/core';
import {BaseButton} from './base-button';

@Component({
  selector: 'app-root',
  imports: [BaseButton],
  template: `<button baseButton>Next <span class="icon arrow-right"></span></button>`,
})
export class App {}
```

Batafsil maʼlumot va bu patterndan foydalanishning boshqa usullari uchun [`<ng-content>` boʻyicha chuqur qoʻllanma](/guide/components/content-projection)ga qarang.
