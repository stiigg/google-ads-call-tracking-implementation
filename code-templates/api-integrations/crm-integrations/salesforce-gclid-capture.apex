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
