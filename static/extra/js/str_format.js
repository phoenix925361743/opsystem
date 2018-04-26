/**
 * Created by Administrator on 2017/11/16.
 */
(function() {
             var chopper = window.chopper = window.chopper || { cultures: {} },
                 math = Math,
                 formatRegExp = /\{(\d+)(:[^\}]+)?\}/g,
                 FUNCTION = "function",
                 STRING = "string",
                 NUMBER = "number",
                 OBJECT = "object",
                 NULL = "null",
                 BOOLEAN = "boolean",
                 UNDEFINED = "undefined",
                 slice = [].slice,
                 globalize = window.Globalize,
                 standardFormatRegExp =  /^(n|c|p|e)(\d*)$/i,
                 literalRegExp = /(\\.)|(['][^']*[']?)|(["][^"]*["]?)/g,
                 commaRegExp = /\,/g,
                 EMPTY = "",
                 POINT = ".",
                 COMMA = ",",
                 SHARP = "#",
                 ZERO = "0",
                 PLACEHOLDER = "??",
                 EN = "en-US",
                 objectToString = {}.toString;
             //cultures
             chopper.cultures["en-US"] = {
                 name: EN,
                 numberFormat: {
                     pattern: ["-n"],
                     decimals: 2,
                     ",": ",",
                     ".": ".",
                     groupSize: [3],
                     percent: {
                         pattern: ["-n %", "n %"],
                         decimals: 2,
                         ",": ",",
                         ".": ".",
                         groupSize: [3],
                         symbol: "%"
                     },
                     currency: {
                         pattern: ["($n)", "$n"],
                         decimals: 2,
                         ",": ",",
                         ".": ".",
                         groupSize: [3],
                         symbol: "$"
                     }
                 },
                 calendars: {
                     standard: {
                         days: {
                             names: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                             namesAbbr: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
                             namesShort: [ "Su", "Mo", "Tu", "We", "Th", "Fr", "Sa" ]
                         },
                         months: {
                             names: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                             namesAbbr: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                         },
                         AM: [ "AM", "am", "AM" ],
                         PM: [ "PM", "pm", "PM" ],
                         patterns: {
                             d: "M/d/yyyy",
                             D: "dddd, MMMM dd, yyyy",
                             F: "dddd, MMMM dd, yyyy h:mm:ss tt",
                             g: "M/d/yyyy h:mm tt",
                             G: "M/d/yyyy h:mm:ss tt",
                             m: "MMMM dd",
                             M: "MMMM dd",
                             s: "yyyy'-'MM'-'ddTHH':'mm':'ss",
                             t: "h:mm tt",
                             T: "h:mm:ss tt",
                             u: "yyyy'-'MM'-'dd HH':'mm':'ss'Z'",
                             y: "MMMM, yyyy",
                             Y: "MMMM, yyyy"
                         },
                         "/": "/",
                         ":": ":",
                         firstDay: 0,
                         twoDigitYearMax: 2029
                     }
                 }
             };
              function findCulture(culture) {
                 if (culture) {
                     if (culture.numberFormat) {
                         return culture;
                     }
                     if (typeof culture === STRING) {
                         var cultures = chopper.cultures;
                         return cultures[culture] || cultures[culture.split("-")[0]] || null;
                     }
                     return null;
                 }
                 return null;
             }
             function getCulture(culture) {
                 if (culture) {
                     culture = findCulture(culture);
                 }
                 return culture || chopper.cultures.current;
             }
             function expandNumberFormat(numberFormat) {
                 numberFormat.groupSizes = numberFormat.groupSize;
                 numberFormat.percent.groupSizes = numberFormat.percent.groupSize;
                 numberFormat.currency.groupSizes = numberFormat.currency.groupSize;
             }
             chopper.culture = function(cultureName) {
                 var cultures = chopper.cultures, culture;
                 if (cultureName !== undefined) {
                     culture = findCulture(cultureName) || cultures[EN];
                     culture.calendar = culture.calendars.standard;
                     cultures.current = culture;
                     if (globalize && !globalize.load) {
                         expandNumberFormat(culture.numberFormat);
                     }
                 } else {
                     return cultures.current;
                 }
             };
             chopper.culture(EN);
             //number formatting
             function formatNumber(number, format, culture) {
                 culture = getCulture(culture);
                 var numberFormat = culture.numberFormat,
                     groupSize = numberFormat.groupSize[0],
                     groupSeparator = numberFormat[COMMA],
                     decimal = numberFormat[POINT],
                     precision = numberFormat.decimals,
                     pattern = numberFormat.pattern[0],
                     literals = [],
                     symbol,
                     isCurrency, isPercent,
                     customPrecision,
                     formatAndPrecision,
                     negative = number < 0,
                     integer,
                     fraction,
                     integerLength,
                     fractionLength,
                     replacement = EMPTY,
                     value = EMPTY,
                     idx,
                     length,
                     ch,
                     hasGroup,
                     hasNegativeFormat,
                     decimalIndex,
                     sharpIndex,
                     zeroIndex,
                     hasZero, hasSharp,
                     percentIndex,
                     currencyIndex,
                     startZeroIndex,
                     start = -1,
                     end;
                 //return empty string if no number
                 if (number === undefined) {
                     return EMPTY;
                 }
                 if (!isFinite(number)) {
                     return number;
                 }
                 //if no format then return number.toString() or number.toLocaleString() if culture.name is not defined
                 if (!format) {
                     return culture.name.length ? number.toLocaleString() : number.toString();
                 }
                 formatAndPrecision = standardFormatRegExp.exec(format);
                 // standard formatting
                 if (formatAndPrecision) {
                     format = formatAndPrecision[1].toLowerCase();
                     isCurrency = format === "c";
                     isPercent = format === "p";
                     if (isCurrency || isPercent) {
                         //get specific number format information if format is currency or percent
                         numberFormat = isCurrency ? numberFormat.currency : numberFormat.percent;
                         groupSize = numberFormat.groupSize[0];
                         groupSeparator = numberFormat[COMMA];
                         decimal = numberFormat[POINT];
                         precision = numberFormat.decimals;
                         symbol = numberFormat.symbol;
                         pattern = numberFormat.pattern[negative ? 0 : 1];
                     }
                     customPrecision = formatAndPrecision[2];
                     if (customPrecision) {
                         precision = +customPrecision;
                     }
                     //return number in exponential format
                     if (format === "e") {
                         return customPrecision ? number.toExponential(precision) : number.toExponential(); // toExponential() and toExponential(undefined) differ in FF #653438.
                     }
                     // multiply if format is percent
                     if (isPercent) {
                         number *= 100;
                     }
                     number = round(number, precision);
                     negative = number < 0;
                     number = number.split(POINT);
                     integer = number[0];
                     fraction = number[1];
                     //exclude "-" if number is negative.
                     if (negative) {
                         integer = integer.substring(1);
                     }
                     value = integer;
                     integerLength = integer.length;
                     //add group separator to the number if it is longer enough
                     if (integerLength >= groupSize) {
                         value = EMPTY;
                         for (idx = 0; idx < integerLength; idx++) {
                             if (idx > 0 && (integerLength - idx) % groupSize === 0) {
                                 value += groupSeparator;
                             }
                             value += integer.charAt(idx);
                         }
                     }
                     if (fraction) {
                         value += decimal + fraction;
                     }
                     if (format === "n" && !negative) {
                         return value;
                     }
                     number = EMPTY;
                     for (idx = 0, length = pattern.length; idx < length; idx++) {
                         ch = pattern.charAt(idx);
                         if (ch === "n") {
                             number += value;
                         } else if (ch === "$" || ch === "%") {
                             number += symbol;
                         } else {
                             number += ch;
                         }
                     }
                     return number;
                 }
                 //custom formatting
                 //
                 //separate format by sections.
                 //make number positive
                 if (negative) {
                     number = -number;
                 }
                 if (format.indexOf("'") > -1 || format.indexOf("\"") > -1 || format.indexOf("\\") > -1) {
                     format = format.replace(literalRegExp, function (match) {
                         var quoteChar = match.charAt(0).replace("\\", ""),
                             literal = match.slice(1).replace(quoteChar, "");
                         literals.push(literal);
                         return PLACEHOLDER;
                     });
                 }
                 format = format.split(";");
                 if (negative && format[1]) {
                     //get negative format
                     format = format[1];
                     hasNegativeFormat = true;
                 } else if (number === 0) {
                     //format for zeros
                     format = format[2] || format[0];
                     if (format.indexOf(SHARP) === -1 && format.indexOf(ZERO) === -1) {
                         //return format if it is string constant.
                         return format;
                     }
                 } else {
                     format = format[0];
                 }
                 percentIndex = format.indexOf("%");
                 currencyIndex = format.indexOf("$");
                 isPercent = percentIndex !== -1;
                 isCurrency = currencyIndex !== -1;
                 //multiply number if the format has percent
                 if (isPercent) {
                     number *= 100;
                 }
                 if (isCurrency && format[currencyIndex - 1] === "\\") {
                     format = format.split("\\").join("");
                     isCurrency = false;
                 }
                 if (isCurrency || isPercent) {
                     //get specific number format information if format is currency or percent
                     numberFormat = isCurrency ? numberFormat.currency : numberFormat.percent;
                     groupSize = numberFormat.groupSize[0];
                     groupSeparator = numberFormat[COMMA];
                     decimal = numberFormat[POINT];
                     precision = numberFormat.decimals;
                     symbol = numberFormat.symbol;
                 }
                 hasGroup = format.indexOf(COMMA) > -1;
                 if (hasGroup) {
                     format = format.replace(commaRegExp, EMPTY);
                 }
                 decimalIndex = format.indexOf(POINT);
                 length = format.length;
                 if (decimalIndex !== -1) {
                     fraction = number.toString().split("e");
                     if (fraction[1]) {
                         fraction = round(number, Math.abs(fraction[1]));
                     } else {
                         fraction = fraction[0];
                     }
                     fraction = fraction.split(POINT)[1] || EMPTY;
                     zeroIndex = format.lastIndexOf(ZERO) - decimalIndex;
                     sharpIndex = format.lastIndexOf(SHARP) - decimalIndex;
                     hasZero = zeroIndex > -1;
                     hasSharp = sharpIndex > -1;
                     idx = fraction.length;
                     if (!hasZero && !hasSharp) {
                         format = format.substring(0, decimalIndex) + format.substring(decimalIndex + 1);
                         length = format.length;
                         decimalIndex = -1;
                         idx = 0;
                     } if (hasZero && zeroIndex > sharpIndex) {
                         idx = zeroIndex;
                     } else if (sharpIndex > zeroIndex) {
                         if (hasSharp && idx > sharpIndex) {
                             idx = sharpIndex;
                         } else if (hasZero && idx < zeroIndex) {
                             idx = zeroIndex;
                         }
                     }
                     if (idx > -1) {
                         number = round(number, idx);
                     }
                 } else {
                     number = round(number);
                 }
                 sharpIndex = format.indexOf(SHARP);
                 startZeroIndex = zeroIndex = format.indexOf(ZERO);
                 //define the index of the first digit placeholder
                 if (sharpIndex === -1 && zeroIndex !== -1) {
                     start = zeroIndex;
                 } else if (sharpIndex !== -1 && zeroIndex === -1) {
                     start = sharpIndex;
                 } else {
                     start = sharpIndex > zeroIndex ? zeroIndex : sharpIndex;
                 }
                 sharpIndex = format.lastIndexOf(SHARP);
                 zeroIndex = format.lastIndexOf(ZERO);
                 //define the index of the last digit placeholder
                 if (sharpIndex === -1 && zeroIndex !== -1) {
                     end = zeroIndex;
                 } else if (sharpIndex !== -1 && zeroIndex === -1) {
                     end = sharpIndex;
                 } else {
                     end = sharpIndex > zeroIndex ? sharpIndex : zeroIndex;
                 }
                 if (start === length) {
                     end = start;
                 }
                 if (start !== -1) {
                     value = number.toString().split(POINT);
                     integer = value[0];
                     fraction = value[1] || EMPTY;
                     integerLength = integer.length;
                     fractionLength = fraction.length;
                     if (negative && (number * -1) >= 0) {
                         negative = false;
                     }
                     //add group separator to the number if it is longer enough
                     if (hasGroup) {
                         if (integerLength === groupSize && integerLength < decimalIndex - startZeroIndex) {
                             integer = groupSeparator + integer;
                         } else if (integerLength > groupSize) {
                             value = EMPTY;
                             for (idx = 0; idx < integerLength; idx++) {
                                 if (idx > 0 && (integerLength - idx) % groupSize === 0) {
                                     value += groupSeparator;
                                 }
                                 value += integer.charAt(idx);
                             }
                             integer = value;
                         }
                     }
                     number = format.substring(0, start);
                     if (negative && !hasNegativeFormat) {
                         number += "-";
                     }
                     for (idx = start; idx < length; idx++) {
                         ch = format.charAt(idx);
                         if (decimalIndex === -1) {
                             if (end - idx < integerLength) {
                                 number += integer;
                                 break;
                             }
                         } else {
                             if (zeroIndex !== -1 && zeroIndex < idx) {
                                 replacement = EMPTY;
                             }
                             if ((decimalIndex - idx) <= integerLength && decimalIndex - idx > -1) {
                                 number += integer;
                                 idx = decimalIndex;
                             }
                             if (decimalIndex === idx) {
                                 number += (fraction ? decimal : EMPTY) + fraction;
                                 idx += end - decimalIndex + 1;
                                 continue;
                             }
                         }
                         if (ch === ZERO) {
                             number += ch;
                             replacement = ch;
                         } else if (ch === SHARP) {
                             number += replacement;
                         }
                     }
                     if (end >= start) {
                         number += format.substring(end + 1);
                     }
                     //replace symbol placeholders
                     if (isCurrency || isPercent) {
                         value = EMPTY;
                         for (idx = 0, length = number.length; idx < length; idx++) {
                             ch = number.charAt(idx);
                             value += (ch === "$" || ch === "%") ? symbol : ch;
                         }
                         number = value;
                     }
                     length = literals.length;
                     if (length) {
                         for (idx = 0; idx < length; idx++) {
                             number = number.replace(PLACEHOLDER, literals[idx]);
                         }
                     }
                 }
                 return number;
             }
             var round = function(value, precision) {
                 precision = precision || 0;
                 value = value.toString().split('e');
                 value = Math.round(+(value[0] + 'e' + (value[1] ? (+value[1] + precision) : precision)));
                 value = value.toString().split('e');
                 value = +(value[0] + 'e' + (value[1] ? (+value[1] - precision) : -precision));
                 return value.toFixed(precision);
             };
             var toString = function(value, fmt, culture) {
                 if (fmt) {
                     if (typeof value === NUMBER) {
                         return formatNumber(value, fmt, culture);
                     }
                 }
                 return value !== undefined ? value : "";
             };
             if (globalize && !globalize.load) {
                 toString = function(value, format, culture) {
                     if ($.isPlainObject(culture)) {
                         culture = culture.name;
                     }
                     return globalize.format(value, format, culture);
                 };
             }
             chopper.format = function(fmt) {
                 var values = arguments;
                 return fmt.replace(formatRegExp, function(match, index, placeholderFormat) {
                     var value = values[parseInt(index, 10) + 1];
                     return toString(value, placeholderFormat ? placeholderFormat.substring(1) : "");
                 });
             };
         })();