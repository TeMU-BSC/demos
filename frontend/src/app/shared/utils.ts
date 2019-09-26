import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { HttpHeaders } from '@angular/common/http';

/**
 * Utils class that contains useful functions to reuse in different components.
 */
export class Utils {

  /**
   * Options that accepts JSON requests and responses
   */
  public static getBasicOptions() {
    return {
      headers: new HttpHeaders({
        Accept: 'application/json'
      })
    }
  }

  /**
   * Generate a valid URI to download a file in JSON format.
   */
  public static generateDownloadJsonUri(results: any, sanitizer: DomSanitizer): SafeUrl {
    const theJsonString: string = JSON.stringify(results);
    const uri: SafeUrl = sanitizer.bypassSecurityTrustUrl(`data:text/json;charset=UTF-8,${encodeURIComponent(theJsonString)}`);
    return uri;
  }

  /**
   * Calculate the average score.
   */
  public static getAverage(scores: number[]) {
    let sum = 0
    scores.forEach((score: number) => {
      sum += score
    })
    return sum / scores.length
  }

  /**
   * Round a number to a given decimal float point. 
   * https://www.jacklmoore.com/notes/rounding-in-javascript/
   * 
   */
  public static round(value: number, decimals: number) {
    return Number(Math.round(Number(value + 'e' + decimals)) + 'e-' + decimals);
  }

}
