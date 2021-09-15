/**
 * Shared module that contains CONSTANTS to access properly to the business
 * data, according to the internal API documentation provided by BSC backend
 * developers.
 *
 * @author Alejandro Asensio <https://github.com/aasensios>
 */

/**
 * Text Mining API URLs to be consumed by the frontend services.
 */
export const TEMU_API_URLS = {
  pos: 'http://localhost:5003',
  translator: 'http://localhost:5001',
  pharmaconer: 'http://localhost:5002',
  ner: 'http://localhost:5000',

  // production: 'http://temu.bsc.es/api'
}

/**
 * Interface with the skeleton of an expected response from
 * Text Mining Unit APIs.
 */
export interface TemuResponse {
  data: any
  message: string
  success: boolean
}
