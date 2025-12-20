/**
 * ⚠️ OPTIONAL INTEGRATION - NOT REQUIRED FOR BASIC SETUP
 * 
 * This Apex code is only needed if you already use Salesforce CRM.
 * CallRail can track offline conversions and send to Google Ads without Salesforce.
 * 
 * Use this only if your business requires:
 * - Enterprise sales pipeline management
 * - Complex multi-month sales cycles
 * - Team collaboration on deals in Salesforce
 * 
 * Most businesses should NOT use this file.
 * Read code-templates/api-integrations/crm-integrations/README.md first.
 */

public class GclidCaptureController {
    public static void captureGclid(String gclid, Id leadId) {
        if (String.isBlank(gclid) || leadId == null) {
            return;
        }

        Lead lead = [SELECT Id, GCLID__c FROM Lead WHERE Id = :leadId LIMIT 1];
        lead.GCLID__c = gclid;
        update lead;
    }
}
